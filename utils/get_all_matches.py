import requests
import json

def fetch_and_save_data(page_number, current_season_year):
    url = f"https://www.balldontlie.io/api/v1/games?seasons[]={current_season_year}&per_page=100&page={page_number}"
    
    try:
        response = requests.get(url)
        response.raise_for_status()  # Raise an HTTPError for bad responses

        result = response.json()
        data = result.get("data", [])

        return data, result.get("meta", {}).get("next_page")
    except requests.exceptions.RequestException as e:
        print(f"Error fetching data from page {page_number}: {e}")
        return None, None

# Function to sort data by date
def sort_data_by_date(data):
    return sorted(data, key=lambda x: x.get("date", ""))

def get_all_matches(write_file, current_season_year):

    # Combine data from all pages into a single list
    all_data = []
    current_page = 1

    # Fetch data until there's no "next_page"
    while True:
        page_data, next_page = fetch_and_save_data(current_page, current_season_year)
        
        if not page_data:
            break
        
        all_data.extend(page_data)
        
        if next_page is None:
            break
        
        current_page += 1

    # Filter data to include only entries with status "Final"
    final_data = [entry for entry in all_data if entry.get("status") == "Final"]

    # Sort the final data by date
    sorted_final_data = sort_data_by_date(final_data)

    # Save sorted data to a single file named test.json
    with open(write_file, "w") as json_file:
        json.dump(sorted_final_data, json_file, indent=2)

    print("[🟢] Successfully filtered and sorted data (status: Final) saved to json.")
    
    return None
