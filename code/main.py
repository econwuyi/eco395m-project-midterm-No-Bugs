from code.data_collection import (
    scrape_puh_rankings,
    collect_sat_tuition,
    scrape_college_earnings,
    ranking_state
)

from code.data_cleaning import process_university_data


def main():
    print("Starting full data collection pipeline...\n")

    print("Step 1: Scraping Public University Rankings...")
    scrape_puh_rankings()

    print("\nStep 2: Collecting SAT and Tuition Data...")
    collect_sat_tuition()

    print("\nStep 3: Scraping College Earnings Data...")
    scrape_college_earnings()

    print("\nStep 4: Collecting State-level Rankings...")
    ranking_state()

    print("\nStep 5: Processing, cleaning, and merging data...")
    process_university_data()

    print("\nData cleaning and processing completed successfully.\n")

    print("\nData collection completed for all modules.\n")

if __name__ == "__main__":
    main()
