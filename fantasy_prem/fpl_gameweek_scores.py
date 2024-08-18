import requests
import json

# make API call for gameweek data and store response
url_bootstrap = "https://fantasy.premierleague.com/api/bootstrap-static/"
r_bs = requests.get(url_bootstrap)
print(f"Status code (bootstrap): {r_bs.status_code}")

# Convert the response object to a list of gameweeks
bs_dict = r_bs.json()
gameweeks = [item['id'] for item in bs_dict['events']]

print(gameweeks)

# make API call for manager IDs and store response
url_league = "https://fantasy.premierleague.com/api/leagues-h2h/147261/standings/"
r_l = requests.get(url_league)
print(f"Status code (league): {r_l.status_code}")

# Convert the response object to a dictionary
entry_dict = r_l.json()
manager_dicts = entry_dict['standings']['results']

# Create blank list for entrant IDs
team_ids = []

# Move each entrant ID to team_id list
for manager_dict in manager_dicts:
    team_ids.append(manager_dict['entry'])

scores_static = []

for gameweek in gameweeks:
    for team_id in team_ids:
        scores_static.append(
            {
                'team_id': team_id,
                'gameweek': gameweek,
                'score': None
            }
        )

print(team_ids)

for team_id in team_ids:
    for gameweek in gameweeks:
        url_p = f"https://fantasy.premierleague.com/api/entry/{team_id}/event/{gameweek}/picks/"
        r_p = requests.get(url_p)
        response_dict = r_p.json()
        scores_dict = response_dict['entry_history']['points']
        
print(scores_dict)