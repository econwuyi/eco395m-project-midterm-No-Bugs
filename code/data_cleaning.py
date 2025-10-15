import pandas as pd
from pathlib import Path


def process_university_data(base_path="artifacts"):
    """
    Process university data by cleaning, merging, analyzing, and saving the final dataset.

    Args:
        base_path (str): Relative path to the directory containing input CSV files
                         and where the output will be saved (default: 'artifacts')

    Returns:
        pd.DataFrame: Cleaned and merged final dataset, or None if an error occurs
    """
    print("Starting university data processing...")

    # Define data paths using relative path from project root
    base_path = Path(__file__).parent.parent / base_path

    # Read all data files
    try:
        usnews_df = pd.read_csv(base_path / "usnews_top50.csv")
        tuition_sat_df = pd.read_csv(base_path / "tuition&sat_top50.csv")
        earnings_df = pd.read_csv(base_path / "graduate_earnings_data.csv")
        puh_df = pd.read_csv(base_path / "PUHranking.csv")
        print("Raw data files loaded successfully!")
    except FileNotFoundError as e:
        print(f"Error: Cannot find data files. Please ensure files are in correct path. {e}")
        return None

    # Clean each dataset
    print("Starting data cleaning...")

    # Clean US News data
    usnews_clean = usnews_df.copy()
    usnews_clean = usnews_clean.rename(columns={
        'institution.displayName': 'school_name',
        'institution.state': 'state',
        'ranking.displayRank': 'display_rank',
        'ranking.sortRank': 'sort_rank',
        'ranking.isTied': 'is_tied'
    })
    usnews_clean['school_name'] = usnews_clean['school_name'].str.strip()
    usnews_clean['display_rank'] = usnews_clean['display_rank'].str.replace('#', '').astype(int)
    usnews_clean['sort_rank'] = pd.to_numeric(usnews_clean['sort_rank'], errors='coerce')
    print(f"US News data cleaned: {len(usnews_clean)} schools")

    # Clean tuition and SAT data
    tuition_sat_clean = tuition_sat_df.copy()
    tuition_sat_clean = tuition_sat_clean.rename(columns={
        'institution.displayName': 'school_name',
        'searchData.tuition.rawValue': 'tuition',
        'searchData.satAvg.rawValue': 'sat_score'
    })
    tuition_sat_clean['school_name'] = tuition_sat_clean['school_name'].str.strip()
    tuition_sat_clean['tuition'] = pd.to_numeric(tuition_sat_clean['tuition'], errors='coerce')
    tuition_sat_clean['sat_score'] = pd.to_numeric(tuition_sat_clean['sat_score'], errors='coerce')
    print(f"Tuition & SAT data cleaned: {len(tuition_sat_clean)} schools")

    # Clean earnings data
    earnings_clean = earnings_df.copy()
    earnings_clean = earnings_clean.rename(columns={
        'Institution': 'school_name',
        'Median Earnings - 6 Years Post-Entry (Scorecard)': 'median_earnings'
    })
    earnings_clean['school_name'] = earnings_clean['school_name'].str.strip()
    earnings_clean['median_earnings'] = pd.to_numeric(earnings_clean['median_earnings'], errors='coerce')
    print(f"Earnings data cleaned: {len(earnings_clean)} schools")

    # Clean historical ranking data
    puh_clean = puh_df.copy()
    puh_clean = puh_clean.rename(columns={
        'University': 'school_name',
        'rk2018': 'ht2018',
        'rk2019': 'ht2019',
        'rk2020': 'ht2020',
        'rk2021': 'ht2021',
        'rk2022': 'ht2022',
        'rk2023': 'ht2023',
        'rk2024': 'ht2024',
        'rk2025': 'ht2025',
        'avgrk': 'avgtk'
    })
    puh_clean['school_name'] = puh_clean['school_name'].str.strip()
    rank_columns = ['ht2018', 'ht2019', 'ht2020', 'ht2021', 'ht2022', 'ht2023', 'ht2024', 'ht2025', 'avgtk']
    for col in rank_columns:
        if col in puh_clean.columns:
            puh_clean[col] = pd.to_numeric(puh_clean[col], errors='coerce')
    print(f"Historical ranking data cleaned: {len(puh_clean)} schools")

    # Merge data step by step
    print("Starting data merging...")
    merged_df = usnews_clean.merge(tuition_sat_clean, on='school_name', how='left')
    print(f"After first merge: {len(merged_df)} schools")
    merged_df = merged_df.merge(earnings_clean, on='school_name', how='left')
    print(f"After second merge: {len(merged_df)} schools")
    merged_df = merged_df.merge(puh_clean, on='school_name', how='left')
    print(f"Final merged dataset: {len(merged_df)} schools")

    # Display basic information about merged results
    print("\nColumns in merged data:", merged_df.columns.tolist())
    print("Data shape:", merged_df.shape)

    # Save cleaned and merged data
    output_path = base_path / "cleaned_merged_dataset.csv"
    merged_df.to_csv(output_path, index=False)
    print(f"\nCleaned data saved to: {output_path}")

    # Analyze the data
    print("\nData analysis:")
    print("First 5 schools in the dataset:")
    print(merged_df[['school_name', 'display_rank', 'tuition', 'sat_score', 'median_earnings']].head())

    # Check for missing SAT scores
    missing_sat = merged_df['sat_score'].isna().sum()
    print(f"\nNumber of schools with missing SAT scores: {missing_sat}")
    if missing_sat > 0:
        print("Schools with missing SAT scores:")
        print(merged_df[merged_df['sat_score'].isna()][['school_name', 'display_rank']])

    # Check for missing earnings data
    missing_earnings = merged_df['median_earnings'].isna().sum()
    print(f"\nNumber of schools with missing earnings data: {missing_earnings}")

    # Check tied rankings
    print("\n=== CHECKING TIED RANKINGS ===")
    tied_schools = merged_df[merged_df['is_tied'] == True]
    print(f"Number of schools with tied rankings: {len(tied_schools)}")
    rank_groups = merged_df.groupby('display_rank').size()
    tied_ranks = rank_groups[rank_groups > 1]
    print("\nTied ranking groups:")
    for rank, count in tied_ranks.items():
        schools = merged_df[merged_df['display_rank'] == rank]['school_name'].tolist()
        print(f"Rank #{rank}: {count} schools - {', '.join(schools)}")
    print("\nRanking comparison (first 15 schools):")
    print(merged_df[['school_name', 'display_rank', 'sort_rank', 'is_tied']].head(15))

    print("\nUniversity data processing completed!")
    return merged_df