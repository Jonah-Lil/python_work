import requests
import json

# make API call and store response
url = "https://fantasy.premierleague.com/api/bootstrap-static/"
r = requests.get(url)
print(f"Status code: {r.status_code}")

# Convert the response object to a dictionary
response_dict = r.json()

# Process results
# readable_contents = json.dumps(response_dict, indent=4)
print(response_dict.keys())

#gameweek_ids = response_dict['events']
# readable_contents = json.dumps(gameweek_ids, indent=4)

# Create list of gameweeks
#gameweeks = []

# for gameweek_id in gameweek_ids:
   # gameweeks.append({gameweek_id['id']})

#for gameweek in gameweeks:
 #   print(f"Gameweek: {gameweek}")