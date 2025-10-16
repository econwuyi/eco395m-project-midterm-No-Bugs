# eco395m-project-midterm-No-Bugs

## Sources of datasets  

### U.S. News & World Report's Best Colleges Rankings  
**Includes:** Tuition fees, SAT score range, location (state), and ranking data.  
**URL:** `https://www.usnews.com/best-colleges/rankings/national-universities?myCollege=national-universities&_sort=myCollege&_sortDirection=asc`

### Public University Honors  
**Includes:** U.S. News school ranking data from 2018 to 2025, and their average rankings.  
**URL:** `https://publicuniversityhonors.com/us-news-rankings-2025-which-universities-have-gained-or-lost-the-most-since-2018/`

### College Transitions  
**Includes:** Multi-period graduate earnings data.  
**URL:** `https://www.collegetransitions.com/dataverse/graduate-earnings/`  

## Running Guide  

**Ensure Dependencies are Installed**: Please make sure you have installed all the libraries listed in `requirements.txt` before proceeding.
**Execute the Main Script**: Run `code/main.py` from the project directory. Since all functions are encapsulated within it, this will automatically restart the entire workflow starting from data scraping.
**Output Locations**: The function will save results in the `artifacts/` and `plot/` folders. The artifacts folder contains:

`artifacts/graduate_earnings_data.csv`, `artifacts/PUHranking.csv`, `artifacts/tuition&sat_top50.csv`, and `artifacts/usnews_top50.csv`, which are the raw table data obtained from web scraping.
`artifacts/cleaned_merged_dataset.csv`, the final cleaned and merged dataset.
`artifacts/regression.csv`, the results of the regression analysis.
The `plot/` folder includes all visualization images generated from the analysis.



## Workflow  

### Step 1: School Rank and State Data Collection

**Contributor:** chenzi JIN  
**File:** `code/data_collection.py`     
**Function:** `fetch_rankings_state()`

- Collects top 50 university rankings and state data from US News API
- Uses official API endpoint with proper sorting by ranking position
- Implements pagination to ensure complete data collection
- Handles JSON data extraction with error handling
- Saves structured data to CSV format using relative paths
- Tested locally with successful generation of rankings dataset

**Output File:**
`artifacts/usnews_top50.csv`

### Step 2: Tuition and SAT Data Collection

**Contributor:** Ralmasood  
**File:** `code/data_collection.py`  
**Function:** `collect_sat_tuition()`

- Scrapes tuition and SAT data for the top 50 U.S. universities using the US News API  
- Handles API pagination and nested JSON traversal to extract key fields  
- Saves results in CSV format under `artifacts/tuition&sat_top50.csv`  
- Includes progress logging and error handling for  
- Tested locally with successful data export   

**Output File:**  
`artifacts/tuition&sat_top50.csv`

### Step 4: Average School Rank Collection

**Contributor:** Yi Wu  
**File:** `code/data_collection.py`  
**Function:** `scrape_puh_rankings()`

- Parses table information from the URL using BeautifulSoup
- Uses regular expressions to match data for 160 schools, including US News rankings from 2018 to 2025 and average rankings
- Stores and cleans the data to create analyzable panel data
- Matches school names, updating top-ranked schools to their official names for easier data cleaning
- Saves results in CSV format under `artifacts/PUHranking.csv`

**Output File:**  
`artifacts/PUHranking.csv`

`
