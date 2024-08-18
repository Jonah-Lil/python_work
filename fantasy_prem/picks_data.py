import requests
import json
from kickoff_league_data import team_ids as t

# Initialize a list to store the results
results = []

# Iterate through each team ID in the list
for team_id in t:
    # Construct the URL for the API call
    url = f"https://fantasy.premierleague.com/api/entry/{team_id}/event/1/picks/"
    
    try:
        # Make the API request
        r = requests.get(url)
        r.raise_for_status()  # Raise an error for bad status codes
        
        # Convert the response to JSON
        player_dict = r.json()
        
        # Append the result to the list
        results.append({
            'team_id': team_id,
            'data': player_dict
        })
    
    except requests.RequestException as e:
        print(f"Error fetching data for team ID {team_id}: {e}")

# Print the results to check them
for result in results:
    # Check the type of result to avoid TypeError
    if isinstance(result, dict):
        print(f"Team ID: {result['team_id']}")
        print(json.dumps(result['data'], indent=4))
        print("\n" + "-"*40 + "\n")
    else:
        print("Unexpected data structure:", result)

