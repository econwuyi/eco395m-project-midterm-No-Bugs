import requests
import csv
import os


def traverse(root, path):
    """Get nested value from dict using dot notation path"""
    value = root
    for segment in path.split("."):
        if segment.isdigit():
            value = value[int(segment)] if len(value) > int(segment) else None
        else:
            value = value.get(segment, None)
    return value


def fetch_usnews_rankings():
    """Scrape top 50 school rankings and states from US News API"""
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
    
    base_url = "https://www.usnews.com/best-colleges/api/search?_sort=schoolName&_sortDirection=asc&_page="
    
    all_schools_data = []
    max_schools = 50
    page = 1
    
    print("Starting US News data collection...")
    
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
                    
                row = {}
                for field in fields:
                    row[field] = traverse(school, field)
                all_schools_data.append(row)
            
            if len(all_schools_data) >= max_schools:
                break
                
            page += 1
            
        except Exception as e:
            print(f"Error: {e}")
            break
    
    print(f"Collected {len(all_schools_data)} schools")
    return all_schools_data


def save_rankings_data(schools_data):
    """Save rankings data to CSV using relative path"""
    fields = [
        "institution.displayName", 
        "institution.state",
        "ranking.displayRank", 
        "ranking.sortRank", 
        "ranking.isTied"
    ]
    
    output_dir = "artifacts"
    output_file = "usnews_top50.csv"
    full_path = os.path.join(output_dir, output_file)
    
    os.makedirs(output_dir, exist_ok=True)
    
    with open(full_path, "w", newline="", encoding="utf-8") as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=fields)
        writer.writeheader()
        writer.writerows(schools_data)
    
    print(f"Saved data to: {full_path}")
    return full_path


def ranking_state():
    """Main function to run data collection"""
    data = fetch_usnews_rankings()
    if data:
        save_rankings_data(data)
        print("Step 1 completed successfully")
    else:
        print("Step 1 failed: No data collected")


if __name__ == "__main__":
    ranking_state()