import pandas as pd
import os
from pathlib import Path

def clean_and_merge_data():
    """
    Main data cleaning function.
    Reads multiple CSV files from artifacts folder, cleans them, and merges into a final dataset.
    
    Returns:
    pd.DataFrame: Cleaned and merged final dataset
    """
    print("Starting data cleaning and merging process...")
    
    # Define data paths (using relative paths)
    base_path = Path(__file__).parent.parent / "artifacts"
    
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
    usnews_clean = _clean_usnews_data(usnews_df)
    tuition_sat_clean = _clean_tuition_sat_data(tuition_sat_df)
    earnings_clean = _clean_earnings_data(earnings_df)
    puh_clean = _clean_puh_data(puh_df)
    
    # Merge data step by step
    print("Starting data merging...")
    
    # Step 1: Merge ranking data with tuition & SAT data (based on school name)
    merged_df = usnews_clean.merge(tuition_sat_clean, on='school_name', how='left')
    print(f"After first merge: {len(merged_df)} schools")
    
    # Step 2: Merge with earnings data
    merged_df = merged_df.merge(earnings_clean, on='school_name', how='left')
    print(f"After second merge: {len(merged_df)} schools")
    
    # Step 3: Merge with historical ranking data
    merged_df = merged_df.merge(puh_clean, on='school_name', how='left')
    print(f"Final merged dataset: {len(merged_df)} schools")
    
    # Display basic information about merged results
    print("\nColumns in merged data:", merged_df.columns.tolist())
    print("Data shape:", merged_df.shape)
    
    # Save cleaned and merged data to artifacts folder
    output_path = base_path / "cleaned_merged_dataset.csv"
    merged_df.to_csv(output_path, index=False)
    print(f"\nCleaned data saved to: {output_path}")
    
    return merged_df

def _clean_usnews_data(df):
    """
    Clean US News ranking data.
    """
    cleaned_df = df.copy()
    
    # Rename columns based on actual data structure
    cleaned_df = cleaned_df.rename(columns={
        'institution.displayName': 'school_name',
        'institution.state': 'state', 
        'ranking.displayRank': 'display_rank',
        'ranking.sortRank': 'sort_rank',
        'ranking.isTied': 'is_tied'
    })
    
    # Clean school names: remove leading/trailing whitespace
    cleaned_df['school_name'] = cleaned_df['school_name'].str.strip()
    
    # Process ranking columns: remove '#' symbol and convert to numeric
    cleaned_df['display_rank'] = cleaned_df['display_rank'].str.replace('#', '').astype(int)
    cleaned_df['sort_rank'] = pd.to_numeric(cleaned_df['sort_rank'], errors='coerce')
    
    print(f"US News data cleaned: {len(cleaned_df)} schools")
    return cleaned_df

def _clean_tuition_sat_data(df):
    """
    Clean tuition and SAT data.
    """
    cleaned_df = df.copy()
    
    # Rename columns based on actual data structure
    cleaned_df = cleaned_df.rename(columns={
        'institution.displayName': 'school_name',
        'searchData.tuition.rawValue': 'tuition',
        'searchData.satAvg.rawValue': 'sat_score'
    })
    
    # Clean school names
    cleaned_df['school_name'] = cleaned_df['school_name'].str.strip()
    
    # Ensure tuition and SAT scores are numeric
    cleaned_df['tuition'] = pd.to_numeric(cleaned_df['tuition'], errors='coerce')
    cleaned_df['sat_score'] = pd.to_numeric(cleaned_df['sat_score'], errors='coerce')
    
    print(f"Tuition & SAT data cleaned: {len(cleaned_df)} schools")
    return cleaned_df

def _clean_earnings_data(df):
    """
    Clean graduate earnings data.
    """
    cleaned_df = df.copy()
    
    # Rename columns
    cleaned_df = cleaned_df.rename(columns={
        'Institution': 'school_name',
        'Median Earnings - 6 Years Post-Entry (Scorecard)': 'median_earnings'
    })
    
    # Clean school names
    cleaned_df['school_name'] = cleaned_df['school_name'].str.strip()
    
    # Ensure earnings are numeric
    cleaned_df['median_earnings'] = pd.to_numeric(cleaned_df['median_earnings'], errors='coerce')
    
    print(f"Earnings data cleaned: {len(cleaned_df)} schools")
    return cleaned_df

def _clean_puh_data(df):
    """
    Clean historical ranking data.
    """
    cleaned_df = df.copy()
    
    # Rename columns based on actual data structure
    cleaned_df = cleaned_df.rename(columns={
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
    
    # Clean school names
    cleaned_df['school_name'] = cleaned_df['school_name'].str.strip()
    
    # Ensure all ranking columns are numeric
    rank_columns = ['ht2018', 'ht2019', 'ht2020', 'ht2021', 'ht2022', 'ht2023', 'ht2024', 'ht2025', 'avgtk']
    for col in rank_columns:
        if col in cleaned_df.columns:
            cleaned_df[col] = pd.to_numeric(cleaned_df[col], errors='coerce')
    
    print(f"Historical ranking data cleaned: {len(cleaned_df)} schools")
    return cleaned_df

# If this file is run directly, execute the cleaning function
if __name__ == "__main__":
    final_data = clean_and_merge_data()
    if final_data is not None:
        print("\nData cleaning and merging completed!")
        print("First 5 schools in the dataset:")
        print(final_data[['school_name', 'display_rank', 'tuition', 'sat_score', 'median_earnings']].head())
        
        # Check for missing SAT scores
        missing_sat = final_data['sat_score'].isna().sum()
        print(f"\nNumber of schools with missing SAT scores: {missing_sat}")
        if missing_sat > 0:
            print("Schools with missing SAT scores:")
            missing_schools = final_data[final_data['sat_score'].isna()][['school_name', 'display_rank']]
            print(missing_schools)
            
        # Check for missing earnings data
        missing_earnings = final_data['median_earnings'].isna().sum()
        print(f"\nNumber of schools with missing earnings data: {missing_earnings}")
        
        # ========== Add tied rankings check ==========
        print("\n=== CHECKING TIED RANKINGS ===")
        
        # Find schools with tied rankings
        tied_schools = final_data[final_data['is_tied'] == True]
        print(f"Number of schools with tied rankings: {len(tied_schools)}")
        
        # Group by display_rank to identify tied ranking groups
        rank_groups = final_data.groupby('display_rank').size()
        tied_ranks = rank_groups[rank_groups > 1]
        
        print("\nTied ranking groups:")
        for rank, count in tied_ranks.items():
            schools = final_data[final_data['display_rank'] == rank]['school_name'].tolist()
            print(f"Rank #{rank}: {count} schools - {', '.join(schools)}")
        
        # Compare display_rank vs sort_rank differences
        print("\nRanking comparison (first 15 schools):")
        comparison = final_data[['school_name', 'display_rank', 'sort_rank', 'is_tied']].head(15)
        print(comparison)
        # ========== End tied rankings check ==========
        
    else:
        print("Data cleaning failed!")