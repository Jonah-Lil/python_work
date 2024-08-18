import requests
import json

# make API call and store response
url = "https://fantasy.premierleague.com/api/leagues-h2h/147261/standings/"
r = requests.get(url)
print(f"Status code: {r.status_code}")

# Convert the response object to a dictionary
response_dict = r.json()
readable_contents = json.dumps(response_dict,indent=4)

# Process results
# print(response_dict.keys())
# print(readable_contents)

# Explore information about the entries
entry_dicts = response_dict['standings']['results']
print(f"Players: {len(entry_dicts)}")

# List of entrant IDs
team_ids = []

# Move each entrant ID to team_id list
for entry_dict in entry_dicts:
    team_ids.append(entry_dict['entry'])

print(team_ids)

gameweeks = []

# List of gameweeks
for i in range(38):
    number = i + 1
    gameweeks.append(number)

