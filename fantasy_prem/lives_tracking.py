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

    # Fetch all records from the 'config' collection to map entry IDs to player names
    config_data = {str(record['entry']): record['player_name'] for record in config_collection.find({})}

    # Initialize the dictionary to track lives for each player
    # Start with 3 lives for all IDs
    lives_data = defaultdict(lambda: defaultdict(lambda: 3))
    previous_gameweek_lives = defaultdict(lambda: defaultdict(lambda: 3))

    # Sort records by gameweek to process in order
    last_man_standing_data.sort(key=lambda x: x['gameweek'])

    # Process each gameweek record
    for record in last_man_standing_data:
        gameweek = str(record['gameweek'])  # Convert gameweek to string
        lowest_score_id = record['id_lowest_score']
        second_lowest_score_id = record['id_second_lowest_score']
        third_lowest_score_id = record['id_third_lowest_score']

        # Get lives from the previous gameweek
        if gameweek != '1':  # Skip for the first gameweek
            previous_lives = lives_data[str(int(gameweek) - 1)]
        else:
            previous_lives = {id_: 3 for id_ in config_data.keys()}

        # Update lives based on the previous gameweek
        for id_ in config_data.keys():
            lives_data[gameweek][id_] = previous_lives.get(id_, 3)

        # List of IDs that lose a life in this gameweek
        ids_losing_life = []
        
        if isinstance(lowest_score_id, int):
            ids_losing_life.append(str(lowest_score_id))
        if isinstance(second_lowest_score_id, int):
            ids_losing_life.append(str(second_lowest_score_id))
        if isinstance(third_lowest_score_id, int):
            ids_losing_life.append(str(third_lowest_score_id))

        # Decrement lives for IDs that appear in the three lowest scores
        for id_ in ids_losing_life:
            if id_:
                lives_data[gameweek][id_] -= 1
                if lives_data[gameweek][id_] < 0:
                    lives_data[gameweek][id_] = 0

    # Prepare the data for insertion into the 'lives_tracker' collection
    lives_records = []

    # Collect all IDs from the config collection
    all_ids = set(config_data.keys())

    # Process each gameweek to create records
    for gameweek, ids_lives in lives_data.items():
        gameweek_record = {
            "gameweek": gameweek,
            "lowest_score": []
        }
        
        # Add IDs with updated lives for this gameweek
        for id_, lives in ids_lives.items():
            gameweek_record["lowest_score"].append({
                "id": int(id_),  # Convert ID to integer
                "lives_remaining": lives
            })

        # Ensure the list is sorted by ID if needed (optional)
        gameweek_record["lowest_score"].sort(key=lambda x: x['id'])

        # Append the record for this gameweek
        lives_records.append(gameweek_record)

    # Clear the 'lives_tracker' collection before inserting new data
    lives_tracker_collection.delete_many({})

    # Insert new data into the 'lives_tracker' collection
    lives_tracker_collection.insert_many(lives_records)

if __name__ == "__main__":
    update_lives(MONGO_URI)