import requests
import json

# make API call and store response
url = "https://fantasy.premierleague.com/api/leagues-h2h/147261/standings/"
r = requests.get(url)
print(f"Status code: {r.status_code}")

# Convert the response object to a dictionary
response_dict = r.json()

# Process results
# print(response_dict.keys())

# print(f"New entries: {response_dict['new_entries']['results']}")

# Explore information about the entries
entry_dicts = response_dict['new_entries']['results']
print(f"New entries returned: {len(entry_dicts)}")

print("\nSelected information about each entrant:")
for entry_dict in entry_dicts:
    print(f"\nID: {entry_dict['entry']}")
    print(f"Team name: {entry_dict['entry_name']}")
    print(f"Joined: {entry_dict['joined_time']}")
    print(f"First name: {entry_dict['player_first_name']}")
    print(f"Last name: {entry_dict['player_last_name']}")

