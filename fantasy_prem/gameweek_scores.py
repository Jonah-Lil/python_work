from pymongo import MongoClient
import certifi
import requests
import os

from king_of_the_hill import get_koh
from lms_v2 import get_lms
from lives_tracking import update_lives

ca = certifi.where()
print(ca)
MONGO_URI = os.getenv('MONGO_URI')
print(MONGO_URI[0:10])

client = MongoClient(
    MONGO_URI,
    tlsCAFile=ca)

def update_managers():
    # make API call for manager IDs and store response
    url_league = "https://fantasy.premierleague.com/api/leagues-h2h/147261/standings/"
    r_l = requests.get(url_league)
    print(f"Status code (league): {r_l.status_code}")

    # Convert the response object to a dictionary
    entry_dict = r_l.json()
    manager_dicts = entry_dict['standings']['results']

    result = client['fpl_live']['config'].delete_many({})
    result = client['fpl_live']['config'].insert_many(manager_dicts)

def get_results():
    url_results = "https://fantasy.premierleague.com/api/leagues-h2h-matches/league/147261/"
    results = []
    page = 1

    while True:
        url = f"{url_results}?page={page}"
        response = requests.get(url)
        data = response.json()

        if 'results' in data:
            results.extend(data['results'])
        
        if not data.get('has_next', False):
            break

        page += 1
    
    result = client['fpl_live']['matches'].delete_many({})
    result = client['fpl_live']['matches'].insert_many(results)

def get_history_id(team_id):
    url = f"https://fantasy.premierleague.com/api/entry/{team_id}/history/"
    r = requests.get(url)
    data = r.json()
    data = data['current']

    for week in data: 
        week['id'] = team_id

    return data


def update_scores():
    result = client['fpl_live']['config'].aggregate([
        {
            '$project': {
                'entry': '$entry', 
                '_id': 0
            }
        }
    ])

    data = list(result)
    ids = [x['entry'] for x in data]

    result = client['fpl_live']['weekly_scores'].delete_many({})

    for id in ids: 
        gameweek_scores = get_history_id(id)
        result = client['fpl_live']['weekly_scores'].insert_many(gameweek_scores)

if __name__ == "__main__":
    update_managers()
    update_scores()
    get_results()
    get_koh()
    get_lms(MONGO_URI)