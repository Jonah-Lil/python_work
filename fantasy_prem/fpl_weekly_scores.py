import requests
import json
from fpl_gameweek_scores import team_ids as t, gameweeks as gw

def fetch_points(team_id, gameweek):
    """Fetch points from the API for a given team_id and gameweek."""
    url = f"https://fantasy.premierleague.com/api/entry/{team_id}/event/{gameweek}/picks/"
    try:
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()
        # Extract points; assuming the points are in the 'picks' section of the response
        points = data.get('points', 0)  # Use 0 if 'points' key is not present
    except requests.RequestException as e:
        points = 0
    return points

def create_gameweek_dict(gw, t):
    """Create a nested dictionary with gameweek and points data."""
    gameweek_dict = {}

    for gameweek in gw:
        for team_id in t:
            points = fetch_points(team_id, gameweek)
            
            if gameweek not in gameweek_dict:
                gameweek_dict[gameweek] = {}
                
            gameweek_dict[gameweek][team_id] = {
                'id': gameweek,
                'score': {
                    'entry': team_id,
                    'points': points
                }
            }
    
    return gameweek_dict

# Generate the dictionary
gameweek_dict = create_gameweek_dict(gw, t)

# Output the dictionary to verify the result
for gameweek, teams in gameweek_dict.items():
    for team_id, data in teams.items():
        print(f"Gameweek {gameweek}, Team ID {team_id}: Points {data['score']['points']}")