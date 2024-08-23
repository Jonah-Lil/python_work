from collections import defaultdict
import heapq
from pymongo import MongoClient
import certifi
import requests
import os

ca = certifi.where()
MONGO_URI = os.getenv('MONGO_URI')

def get_lms(MONGO_URI):
    """
    Fetches data from the 'weekly_scores' collection in the 'fpl_live' database,
    processes it to determine the round type and scores for each gameweek,
    and inserts the results into the 'last_man_standing' collection in the 'fpl_live' database.

    Args:
    mongo_uri (str): MongoDB connection URI.
    """
    # Connect to MongoDB
    client = MongoClient(
    MONGO_URI,
    tlsCAFile=ca)
    db = client['fpl_live']
    weekly_scores_collection = db['weekly_scores']
    last_man_standing_collection = db['last_man_standing']

    # Fetch data from the 'weekly_scores' collection and convert it to a list of dictionaries
    source_data = list(weekly_scores_collection.find({}))  # Retrieves all documents from the collection

    # Gameweek types
    single_gameweeks = [1, 2, 5, 9, 12, 13, 16, 25, 26, 29, 30, 37, 38]
    double_gameweeks = [3, 6, 7, 8, 14, 15, 17, 19, 20, 21, 23, 27, 31, 32, 33, 34, 36]
    triple_gameweeks = [4, 10, 11, 18, 22, 24, 28, 35]

    # Function to determine the round type
    def get_round_type(event):
        if event in single_gameweeks:
            return 'Single'
        elif event in double_gameweeks:
            return 'Double'
        elif event in triple_gameweeks:
            return 'Triple'
        else:
            return 'unknown'

    # Organize the source data by gameweek
    gameweek_data = defaultdict(list)
    for record in source_data:
        event = record['event']
        gameweek_data[event].append(record)

    # Create the output list
    output = []

    for gameweek in range(1, 39):
        records = gameweek_data[gameweek]
        round_type = get_round_type(gameweek)
        
        # Default values for all fields
        lowest_score_id = second_lowest_score_id = third_lowest_score_id = None
        lowest_score = second_lowest_score = third_lowest_score = None

        if records:
            # Sort records by points
            sorted_records = sorted(records, key=lambda x: x['points'])
            
            if round_type == 'Single':
                # Single round type: record only the lowest score
                lowest = sorted_records[0]
                lowest_score_id = lowest['id']
                lowest_score = lowest['points']

            elif round_type == 'Double':
                # Double round type: record lowest and second-lowest scores
                if len(sorted_records) > 0:
                    lowest = sorted_records[0]
                    lowest_score_id = lowest['id']
                    lowest_score = lowest['points']
                if len(sorted_records) > 1:
                    second_lowest = sorted_records[1]
                    second_lowest_score_id = second_lowest['id']
                    second_lowest_score = second_lowest['points']

            elif round_type == 'Triple':
                # Triple round type: record lowest, second-lowest, and third-lowest scores
                if len(sorted_records) > 0:
                    lowest = sorted_records[0]
                    lowest_score_id = lowest['id']
                    lowest_score = lowest['points']
                if len(sorted_records) > 1:
                    second_lowest = sorted_records[1]
                    second_lowest_score_id = second_lowest['id']
                    second_lowest_score = second_lowest['points']
                if len(sorted_records) > 2:
                    third_lowest = sorted_records[2]
                    third_lowest_score_id = third_lowest['id']
                    third_lowest_score = third_lowest['points']

        # Build the dictionary for this gameweek
        output.append({
            "gameweek": gameweek,
            "round_type": round_type,
            "id_lowest_score": lowest_score_id,
            "id_second_lowest_score": second_lowest_score_id if round_type in ['Double', 'Triple'] else None,
            "id_third_lowest_score": third_lowest_score_id if round_type == 'Triple' else None,
            "lowest_score": lowest_score,
            "second_lowest_score": second_lowest_score if round_type in ['Double', 'Triple'] else None,
            "third_lowest_score": third_lowest_score if round_type == 'Triple' else None
        })

    # Insert the results into the 'last_man_standing' collection
    result = last_man_standing_collection.delete_many({})
    result = last_man_standing_collection.insert_many(output)

if __name__ == "__main__":
    get_lms(MONGO_URI)