from pymongo import MongoClient
import certifi
import requests
import os
import json

ca = certifi.where()
print(ca)
MONGO_URI = os.getenv('MONGO_URI')

client = MongoClient(
    MONGO_URI,
    tlsCAFile=ca)

def get_player_data():
    # Make API call for player element IDs
    url = "https://fantasy.premierleague.com/api/bootstrap-static/"
    r = requests.get(url)
    print(f"Status code (league): {r.status_code}")

    # Convert the response object to a dictionary
    bootstrap_dict = r.json()
    player_dicts = bootstrap_dict['elements']

    result = client['fpl_live']['individual_player_data'].delete_many({})
    result = client['fpl_live']['individual_player_data'].insert_many(player_dicts)

if __name__ == "__main__":
    get_player_data()