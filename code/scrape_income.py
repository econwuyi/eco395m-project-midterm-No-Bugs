import pandas as pd
import requests

URL = "https://www.collegetransitions.com/dataverse/graduate-earnings/?utm_source=chatgpt.com"
TARGET_COLUMN_INSTITUTION = 'Institution'
TARGET_COLUMN_EARNINGS = 'Median Earnings - 6 Years Post-Entry (Scorecard)'
OUTPUT_FILENAME = 'graduate_earnings_data.csv'

def scrape_college_earnings(url, institution_col, earnings_col, output_file):
    print("Fetching web content...")
    
    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/118.0.0.0 Safari/537.36',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
        'Accept-Language': 'en-US,en;q=0.5',
        'Connection': 'keep-alive',
        'Referer': 'https://www.google.com/',
        'Upgrade-Insecure-Requests': '1'
    }
    
    try:
        response = requests.get(url, headers=headers, timeout=15)
        response.raise_for_status()

        print("Parsing tables from web page...")
        tables = pd.read_html(response.text)

        if not tables:
            print("Error: No tables found on the web page.")
            return

        df = tables[0]
        required_columns = [institution_col, earnings_col]
        missing_columns = [col for col in required_columns if col not in df.columns]

        if missing_columns:
            print(f"Initial table is missing required columns. Trying other tables...")
            for table in tables:
                if institution_col in table.columns and earnings_col in table.columns:
                    df = table
                    break
            else:
                print("Error: Could not find a table containing the required columns.")
                return

        result_df = df[[institution_col, earnings_col]].dropna(how='all')

        print("Cleaning earnings data by removing '$' and converting to numeric...")
        result_df[earnings_col] = (
            result_df[earnings_col]
            .astype(str)
            .str.replace('$', '', regex=False)
            .str.replace(',', '', regex=False)
        )

        result_df[earnings_col] = pd.to_numeric(result_df[earnings_col], errors='coerce')
        result_df = result_df.dropna(subset=[earnings_col]).reset_index(drop=True)

        result_df.to_csv(output_file, index=False)
        print(" Scraping successful!")
        print(f" Data saved to file: {output_file}")
        print(result_df.head())

    except Exception as e:
        print(f" Error: {e}")

if __name__ == "__main__":
    scrape_college_earnings(URL, TARGET_COLUMN_INSTITUTION, TARGET_COLUMN_EARNINGS, OUTPUT_FILENAME)
