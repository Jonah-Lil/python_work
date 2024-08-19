import requests
import json

def fetch_all_pages(base_url):
    results = []
    page = 1

    while True:
        # Construct the URL with the current page number
        url = f"{base_url}?page={page}"
        
        # Make the API request
        response = requests.get(url)
        data = response.json()

        # Check if we received results
        if 'results' in data:
            results.extend(data['results'])

        # Check if there is another page
        if not data.get('has_next', False):
            break

        # Move to the next page
        page += 1

    return results

# URL of the API
base_url = "https://fantasy.premierleague.com/api/leagues-h2h-matches/league/147261/"

# Fetch all pages of results
all_results = fetch_all_pages(base_url)

# Print results in a readable format
print(json.dumps(all_results, indent=4))