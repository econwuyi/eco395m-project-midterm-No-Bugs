import requests
from bs4 import BeautifulSoup
import re
import csv
import pandas as pd
import os

def scrape_puh_rankings(
        url="https://publicuniversityhonors.com/us-news-rankings-2025-which-universities-have-gained-or-lost-the-most-since-2018/",
        output_file="artifacts/PUHranking.csv"):
    """
    Scrapes the website of Public University Honors for university rankings data and saves it to a CSV file.

    Args:
    url (str): The targeted URL.
    output_file (str): The path to the output CSV file.

    Returns:
    str: The path of the saved CSV.

    Data in the CSV:
    University: The name of the university, with top 50 official names.
    rk[year]: The ranking of the university in US. News Best National Universities Rankings of that [year].
    avgrk: The average ranking of the university in US. News Best National Universities Rankings through 2018 to 2025.

    Total Number of Observations: 160

    """
    # Send request to the URL & examine whether it works well
    response = requests.get(url)
    response.raise_for_status()

    # Decode the HTML with BeautifulSoup
    soup = BeautifulSoup(response.content, "html.parser")

    # Find the first table on the page
    table = soup.find("table")

    # Find all row elements whose "class" contains "row-\d+"
    rows = table.find_all("tr", attrs={"class": re.compile(r"row-\d+")})

    # Find the row number and <tr> needed from 4 to 163
    filtered_rows = []
    for tr in rows:
        classes = tr.get("class")
        # For there are two classes
        for cls in classes:
            row_match = re.search(r"row-(\d+)", cls)
            if row_match:
                row_num = int(row_match.group(1))
                if 4 <= row_num <= 163:
                    filtered_rows.append((row_num, tr))
                    break

    # Sort by row number
    filtered_rows.sort(key=lambda x: x[0])

    # Collect data from <tr> of each row
    data = []
    for row_num, tr in filtered_rows:
        # Find the specific tds
        td1 = tr.find("td", class_="column-1")
        td2 = tr.find("td", class_="column-2")
        td3 = tr.find("td", class_="column-3")
        td4 = tr.find("td", class_="column-4")
        td5 = tr.find("td", class_="column-5")
        td6 = tr.find("td", class_="column-6")
        td7 = tr.find("td", class_="column-7")
        td8 = tr.find("td", class_="column-8")
        td9 = tr.find("td", class_="column-9")
        td10 = tr.find("td", class_="column-10")

        # Get text, strip whitespace
        col1_text = td1.get_text(strip=True) if td1 else "N/A"
        col2_text = td2.get_text(strip=True) if td2 else "N/A"
        col3_text = td3.get_text(strip=True) if td3 else "N/A"
        col4_text = td4.get_text(strip=True) if td4 else "N/A"
        col5_text = td5.get_text(strip=True) if td5 else "N/A"
        col6_text = td6.get_text(strip=True) if td6 else "N/A"
        col7_text = td7.get_text(strip=True) if td7 else "N/A"
        col8_text = td8.get_text(strip=True) if td8 else "N/A"
        col9_text = td9.get_text(strip=True) if td9 else "N/A"
        col10_text = td10.get_text(strip=True) if td10 else "N/A"

        # Mapping university names to full official names
        name_mapping = {
            "Princeton": "Princeton University",
            "MIT": "Massachusetts Institute of Technology",
            "Harvard": "Harvard University",
            "Stanford": "Stanford University",
            "Yale": "Yale University",
            "Caltech": "California Institute of Technology",
            "Duke": "Duke University",
            "Johns Hopkins": "Johns Hopkins University",
            "Northwestern": "Northwestern University",
            "Penn": "University of Pennsylvania",
            "Chicago": "University of Chicago",
            "Cornell": "Cornell University",
            "Brown": "Brown University",
            "Columbia": "Columbia University",
            "UCLA": "University of California, Los Angeles",
            "Dartmouth": "Dartmouth College",
            "UC Berkeley": "University of California, Berkeley",
            "Rice": "Rice University",
            "Vanderbilt": "Vanderbilt University",
            "Notre Dame": "University of Notre Dame",
            "Michigan": "University of Michigan--Ann Arbor",
            "Washington Univ": "Washington University in St. Louis",
            "Carnegie Mellon": "Carnegie Mellon University",
            "Georgetown": "Georgetown University",
            "Emory": "Emory University",
            "Virginia": "University of Virginia",
            "North Carolina": "University of North Carolina--Chapel Hill",
            "USC": "University of Southern California",
            "UC San Diego": "University of California, San Diego",
            "Florida": "University of Florida",
            "UT Austin": "The University of Texas--Austin",
            "NYU": "New York University",
            "UC Davis": "University of California, Davis",
            "UC Irvine": "University of California, Irvine",
            "Georgia Tech": "Georgia Institute of Technology",
            "Illinois": "University of Illinois Urbana-Champaign",
            "Boston College": "Boston College",
            "Tufts": "Tufts University",
            "UC Santa Barbara": "University of California, Santa Barbara",
            "UW Madison": "University of Wisconsin--Madison",
            "Rutgers": "Rutgers University--New Brunswick",
            "Boston Univ": "Boston University",
            "Ohio St": "The Ohio State University",
            "Maryland": "University of Maryland, College Park",
            "Rochester": "University of Rochester",
            "Washington": "University of Washington",
            "Purdue": "Purdue University--Main Campus",
            "Georgia": "University of Georgia",
            "Lehigh": "Lehigh University",
            "Northeastern": "Northeastern University"
        }
        university_name = name_mapping.get(col1_text, col1_text)

        data.append({
            "University": university_name,
            "rk2018": col2_text,
            "rk2019": col3_text,
            "rk2020": col4_text,
            "rk2021": col5_text,
            "rk2022": col6_text,
            "rk2023": col7_text,
            "rk2024": col8_text,
            "rk2025": col9_text,
            "avgrk": col10_text
        })

    # Write into a CSV file
    with open(output_file, "w", newline="", encoding="utf-8") as csvfile:
        fieldnames = ["University", "rk2018", "rk2019", "rk2020", "rk2021", "rk2022", "rk2023", "rk2024", "rk2025", "avgrk"]
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(data)
    print(f"\nScraped {len(data)} rows. Data saved to '{output_file}'.")

    return output_file



def scrape_usnews_sat_tuition(
        
url="https://www.usnews.com/best-colleges/rankings/national-universities",
        output_file="artifacts/sat_tuition.csv"):
    """
    Scrapes tuition fees and SAT score ranges for the Top 50 U.S. News 
2026
    Best National Universities and saves them to a CSV file.

    Args:
        url (str): The targeted U.S. News URL.
        output_file (str): The path to save the output CSV.

    Returns:
        str: Path of the saved CSV.
    """
    

    headers = {"User-Agent": "Mozilla/5.0"}
    response = requests.get(url, headers=headers)
    response.raise_for_status()

    soup = BeautifulSoup(response.content, "html.parser")
    universities = []
    cards = soup.select("div.Block-flzCty")

    for i, block in enumerate(cards[:50]):  # limit to top 50
        name_el = block.select_one("h3.Heading-sc-1w5vxap-0")
        rank_el = block.select_one("span.RankList_rank__G2aWY")
        tuition_el = block.find(string=lambda t: "Tuition" in t or "")
        sat_el = block.find(string=lambda t: "SAT" in t or "")

        name = name_el.get_text(strip=True) if name_el else "N/A"
        rank = rank_el.get_text(strip=True) if rank_el else "N/A"
        tuition = tuition_el.strip() if tuition_el else "N/A"
        sat = sat_el.strip() if sat_el else "N/A"

        universities.append({
            "University": name,
            "Rank": rank,
            "Tuition": tuition,
            "SAT_Range": sat
        })

    df = pd.DataFrame(universities)
    df.to_csv(output_file, index=False, encoding="utf-8")
    print(f"Scraped {len(df)} universities. Data saved to '{output_file}'.")
    return output_file


def scrape_college_earnings():
    URL = "https://www.collegetransitions.com/dataverse/graduate-earnings/?utm_source=chatgpt.com"
    TARGET_COLUMN_INSTITUTION = "Institution"
    TARGET_COLUMN_EARNINGS = "Median Earnings - 6 Years Post-Entry (Scorecard)"
    OUTPUT_FILENAME = "artifacts/graduate_earnings_data.csv"

    print("Fetching web content...")

    headers = {
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/118.0.0.0 Safari/537.36",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
        "Accept-Language": "en-US,en;q=0.5",
        "Connection": "keep-alive",
        "Referer": "https://www.google.com/",
        "Upgrade-Insecure-Requests": "1"
    }

    try:
        response = requests.get(URL, headers=headers, timeout=15)
        response.raise_for_status()

        print("Parsing tables from web page...")
        tables = pd.read_html(response.text)

        if not tables:
            print("Error: No tables found on the web page.")
            return

        df = tables[0]
        required_columns = [TARGET_COLUMN_INSTITUTION, TARGET_COLUMN_EARNINGS]
        missing_columns = [col for col in required_columns if col not in df.columns]

        if missing_columns:
            print(f"Initial table is missing required columns. Trying other tables...")
            for table in tables:
                if TARGET_COLUMN_INSTITUTION in table.columns and TARGET_COLUMN_EARNINGS in table.columns:
                    df = table
                    break
            else:
                print("Error: Could not find a table containing the required columns.")
                return

        result_df = df[[TARGET_COLUMN_INSTITUTION, TARGET_COLUMN_EARNINGS]].dropna(how="all")

        print("Cleaning earnings data by removing '$' and converting to numeric...")
        result_df[TARGET_COLUMN_EARNINGS] = (
            result_df[TARGET_COLUMN_EARNINGS]
            .astype(str)
            .str.replace("$", "", regex=False)
            .str.replace(",", "", regex=False)
        )

        result_df[TARGET_COLUMN_EARNINGS] = pd.to_numeric(result_df[TARGET_COLUMN_EARNINGS], errors="coerce")
        result_df = result_df.dropna(subset=[TARGET_COLUMN_EARNINGS]).reset_index(drop=True)

        result_df.to_csv(OUTPUT_FILENAME, index=False)
        print(" Scraping successful!")
        print(f" Data saved to file: {OUTPUT_FILENAME}")
        print(result_df.head())

    except Exception as e:
        print(f" Error: {e}")



def ranking_state():
    """Scrape top 50 school rankings from US News API and save to CSV"""
    fields = [
        "institution.displayName",
        "institution.state",
        "ranking.displayRank",
        "ranking.sortRank",
        "ranking.isTied"
    ]

    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
    }

    base_url = "https://www.usnews.com/best-colleges/api/search?_sort=ranking.sortRank&_sortDirection=asc&_page="
    output_dir = "artifacts"
    output_file = "usnews_top50.csv"
    full_path = os.path.join(output_dir, output_file)
    max_schools = 50
    page = 1
    all_schools_data = []

    print("Starting US News data collection...")

    # Helper function to traverse nested dictionary
    def traverse(root, path):
        value = root
        for segment in path.split("."):
            if segment.isdigit():
                value = value[int(segment)] if len(value) > int(segment) else None
            else:
                value = value.get(segment, None)
        return value

    # Fetch data
    while len(all_schools_data) < max_schools:
        url = f"{base_url}{page}"
        print(f"Fetching page {page}...")

        try:
            resp = requests.get(url, headers=headers, timeout=10)
            print(f"Response status: {resp.status_code}")

            if resp.status_code != 200:
                break

            json_data = resp.json()
            items = json_data.get("data", {}).get("items", [])
            print(f"Found {len(items)} schools on page {page}")

            if not items:
                break

            for school in items:
                if len(all_schools_data) >= max_schools:
                    break
                row = {field: traverse(school, field) for field in fields}
                all_schools_data.append(row)

            page += 1

        except Exception as e:
            print(f"Error: {e}")
            break

    print(f"Collected {len(all_schools_data)} schools")

    # Save data to CSV
    if all_schools_data:
        os.makedirs(output_dir, exist_ok=True)
        with open(full_path, "w", newline="", encoding="utf-8") as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=fields)
            writer.writeheader()
            writer.writerows(all_schools_data)
        print(f"Saved data to: {full_path}")
        print("Step 1 completed successfully")
    else:
        print("Step 1 failed: No data collected")

