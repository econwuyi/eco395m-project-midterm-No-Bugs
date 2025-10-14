"""
Step 2 — Scrape tuition fees and SAT score ranges
for the Top 50 U.S. News National Universities (2026).
"""

import requests
from bs4 import BeautifulSoup
import pandas as pd


def scrape_usnews_top50():
    """Base function setup for Top 50 US News scraper"""
        url = 
"https://www.usnews.com/best-colleges/rankings/national-universities"
    headers = {"User-Agent": "Mozilla/5.0"}
    response = requests.get(url, headers=headers)

    if response.status_code != 200:
        raise Exception("Failed to fetch data from U.S. News")

    soup = BeautifulSoup(response.text, "lxml")
    print("Page fetched and parsed successfully")


if __name__ == "__main__":
    scrape_usnews_top50()

