from pymongo import MongoClient
import certifi
import requests
import os

ca = certifi.where()
MONGO_URI = os.getenv('MONGO_URI')

client = MongoClient(
    MONGO_URI,
    tlsCAFile=ca)

def get_koh(initial_king = 1652909):
    """
    Function to calculate the king of the hill for each gameweek
    """

    # get the matches
    result = client['fpl_live']['matches'].aggregate([
        {
            '$addFields': {
                'hasOccoured': {
                    '$and': [
                        {
                            '$ne': [
                                '$entry_1_points', 0
                            ]
                        }, {
                            '$ne': [
                                '$entry_2_points', 0
                            ]
                        }
                    ]
                }
            }
        }, {
            '$match': {
                'hasOccoured': True
            }
        }
    ])
    data = list(result)

    koh_results = []

    gameweeks = [x['event'] for x in data]


    for gameweek in range(1, max(gameweeks) + 1):
        week_matches = [x for x in data if x['event'] == gameweek]

        if gameweek == 1:
            king = initial_king
        else:
            king = koh_results[-1]['next_king']

        for match in week_matches:
            if match['entry_1_entry'] == king or match['entry_2_entry'] == king:
                koh_match = match
                king_number = 1 if koh_match['entry_1_entry'] == king else 2
                op_number = 2 if king_number == 1 else 1
                op_entry = koh_match[f'entry_{op_number}_entry']
                king_result = 'loss' if koh_match[f'entry_{king_number}_loss'] == 1 else 'win'

                koh_results.append({
                    'gameweek': gameweek,
                    'king': king,
                    'opponent': op_entry,
                    'result': king_result,
                    'next_king': king if king_result == 'loss' else op_entry
                })

                break

    result = client['fpl_live']['king_of_hill_results'].delete_many({})
    result = client['fpl_live']['king_of_hill_results'].insert_many(koh_results)
                
if __name__ == "__main__":
    get_koh()

