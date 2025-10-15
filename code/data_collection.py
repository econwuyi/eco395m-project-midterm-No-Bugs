import requests
from bs4 import BeautifulSoup
import re
import csv


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
    University: The name of the university.
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

        data.append({
            "University": col1_text,
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