from pymongo import MongoClient
from collections import defaultdict
import certifi
import requests
import os

ca = certifi.where()
MONGO_URI = os.getenv('MONGO_URI')

def update_lives(MONGO_URI):
    """
    Updates the number of lives for each ID based on their appearance in each gameweek
    and stores the results in the 'lives_tracker' collection.

    Args:
    mongo_uri (str): MongoDB connection URI.
    """
    # Connect to MongoDB
    client = MongoClient(
    MONGO_URI,
    tlsCAFile=ca)
    db = client['fpl_live']
    last_man_standing_collection = db['last_man_standing']
    lives_tracker_collection = db['lives_tracker']
    config_collection = db['config']

    # Fetch all records from the 'last_man_standing' collection
    last_man_standing_data = list(last_man_standing_collection.find({}))

    # Fetch all records from the 'config' collection to map IDs to player names
    config_data = {str(record['id']): record['player_name'] for record in config_collection.find({})}

    # Initialize the nested dictionary
    lives_data = defaultdict(lambda: defaultdict(lambda: 3))  # Starts with 3 lives for each ID

    # Process each gameweek record
    for record in last_man_standing_data:
        gameweek = str(record['gameweek'])  # Convert gameweek to string
        lowest_score_id = record['id_lowest_score']
        second_lowest_score_id = record['id_second_lowest_score']
        third_lowest_score_id = record['id_third_lowest_score']

        # List of IDs that lose a life in this gameweek
        ids_losing_life = []
        
        if isinstance(lowest_score_id, int):
            ids_losing_life.append(str(lowest_score_id))
        if isinstance(second_lowest_score_id, int):
            ids_losing_life.append(str(second_lowest_score_id))
        if isinstance(third_lowest_score_id, int):
            ids_losing_life.append(str(third_lowest_score_id))

        for id_ in ids_losing_life:
            if id_:  # Ensure id_ is not empty or None
                # Decrement lives if this ID appears in the gameweek
                lives_data[gameweek][id_] -= 1

                # Ensure lives do not go below 0
                if lives_data[gameweek][id_] < 0:
                    lives_data[gameweek][id_] = 0

    # Prepare the data for insertion into the 'lives_tracker' collection
    lives_records = []

    # Collect all IDs across all gameweeks
    all_ids = set()
    for gameweek, ids_lives in lives_data.items():
        all_ids.update(ids_lives.keys())

    # Add records for each ID for each gameweek
    for record in last_man_standing_data:
        gameweek = str(record['gameweek'])  # Convert gameweek to string
        for id_ in all_ids:
            if id_ not in lives_data[gameweek]:
                # If ID did not record one of the three lowest scores, it still has full lives
                lives_data[gameweek][id_] = 3

    # Prepare the final records for insertion
    for gameweek, ids_lives in lives_data.items():
        for id_, lives in ids_lives.items():
            lives_records.append({
                "gameweek": gameweek,
                "lowest_score": {
                    "id": int(id_),  # Convert ID to integer
                    "lives_remaining": lives
                }
            })

    # Clear the 'lives_tracker' collection before inserting new data
    lives_tracker_collection.delete_many({})

    # Insert new data into the 'lives_tracker' collection
    lives_tracker_collection.insert_many(lives_records)

if __name__ == "__main__":
    update_lives(MONGO_URI)