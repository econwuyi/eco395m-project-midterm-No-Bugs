"""
Step 2 — Scrape tuition fees and SAT score ranges
for the Top 50 U.S. News National Universities (2026).
"""

import requests
from bs4 import BeautifulSoup
import pandas as pd


def scrape_usnews_top50():
    """
    Scrapes school name, rank, tuition, and SAT range
    for the top 50 national universities from the U.S. News 2026 rankings.
    Saves results to ./artifacts/usnews_top50.csv
    """
    url = 
"https://www.usnews.com/best-colleges/rankings/national-universities"
    headers = {"User-Agent": "Mozilla/5.0"}
    response = requests.get(url, headers=headers)
    if response.status_code != 200:
        raise Exception("Failed to fetch data from U.S. News")

    soup = BeautifulSoup(response.text, "lxml")
    schools = []

    for i, block in enumerate(soup.select("div.Block-fIczTy")):
        if i >= 50:  # Limit to top 50 universities
            break
        name = block.select_one("h3.Heading-sc-1w5vxk2-0")
        rank = block.select_one("span.RankList_rank__G2awV")
        tuition = block.find(string=lambda t: "Tuition" in t or "")
        sat = block.find(string=lambda t: "SAT" in t or "")
        if name and rank:
            schools.append({
                "School": name.text.strip(),
                "Rank": rank.text.strip("#"),
                "Tuition": tuition.strip() if tuition else "",
                "SAT_Range": sat.strip() if sat else ""
            })

    df = pd.DataFrame(schools)
    df.to_csv("./artifacts/usnews_top50.csv", index=False)
    print(f"Saved {len(df)} records to ./artifacts/usnews_top50.csv")


if __name__ == "__main__":
    scrape_usnews_top50()

