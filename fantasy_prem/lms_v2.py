from collections import defaultdict
import heapq
from pymongo import MongoClient
import certifi
import requests
import os
import polars as pl

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
    diff_data = list(db['matches'].aggregate([
        {
            '$addFields': {
                'entry_1_diff': {
                    '$subtract': [
                        '$entry_1_points', '$entry_2_points'
                    ]
                }, 
                'entry_2_diff': {
                    '$subtract': [
                        '$entry_2_points', '$entry_1_points'
                    ]
                }
            }
        }
    ]))

    # Create a DataFrame from the source data
    events = [x['event'] for x in diff_data if (x['entry_1_total'] + x['entry_2_total']) > 0] + [x['event'] for x in diff_data if (x['entry_1_total'] + x['entry_2_total']) > 0]
    diffs = [x['entry_1_diff'] for x in diff_data if (x['entry_1_total'] + x['entry_2_total']) > 0] + [x['entry_2_diff'] for x in diff_data if (x['entry_1_total'] + x['entry_2_total']) > 0]
    points = [x['entry_1_points'] for x in diff_data if (x['entry_1_total'] + x['entry_2_total']) > 0] + [x['entry_2_points'] for x in diff_data if (x['entry_1_total'] + x['entry_2_total']) > 0]
    entry = [x['entry_1_entry'] for x in diff_data if (x['entry_1_total'] + x['entry_2_total']) > 0] + [x['entry_2_entry'] for x in diff_data if (x['entry_1_total'] + x['entry_2_total']) > 0]

    diff_df = pl.DataFrame(
        {
            'event': events,
            'entry': entry,
            'diff': diffs,
            'points': points
        }
    )

    # Gameweek types
    single_gameweeks = [1, 2, 5, 9, 12, 13, 16, 25, 26, 29, 30, 37, 38]
    double_gameweeks = [3, 6, 7, 8, 14, 15, 17, 19, 20, 21, 23, 27, 31, 32, 33, 34, 36]
    triple_gameweeks = [4, 10, 11, 18, 22, 24, 28, 35]
    init_lives = 3

    elim_df = pl.DataFrame(
        {
            'event': single_gameweeks + double_gameweeks + triple_gameweeks,
            'elims': [1] * len(single_gameweeks) + [2] * len(double_gameweeks) + [3] * len(triple_gameweeks)
        }
    )

    # Join the elimination DataFrame with the main DataFrame
    diff_df = diff_df.join(elim_df, on='event', how='left')
    diff_df = diff_df.sort(['event', 'points', 'diff'], descending=[False, False, False])

    diff_df_filled = pl.DataFrame()

    for event in range(1, 39):
        diff_df_week = diff_df.filter(pl.col('event') == event)
        diff_df_week = diff_df_week.filter(pl.col('points') != 0)

        # break loop if no data for the event
        if diff_df_week.shape[0] == 0:
            break

        if event == 1:
            # first gw, set lives to 3
            diff_df_week = diff_df_week.with_columns(
                pl.lit(init_lives).alias('lives_start')
            )
        else:
            # join with previous week to get lives_start for the current week
            last_week = diff_df_filled.filter(pl.col('event') == (event-1)).select(['entry', 'lives_end'])
            diff_df_week = diff_df_week.join(last_week, on='entry', how='left')
            diff_df_week = diff_df_week.with_columns(
                pl.when(pl.col('lives_end').is_null()).then(0).otherwise(pl.col('lives_end')).alias('lives_start')
            )
            diff_df_week = diff_df_week.drop('lives_end')
        
        # filter out entries with no lives
        diff_df_week = diff_df_week.filter(pl.col('lives_start') > 0)

        # calculate lives lost and lives end for the week
        diff_df_week = (
            diff_df_week
            .with_row_index(offset=1)
            .with_columns(
                (pl.col('index') <= pl.col('elims')).cast(pl.Int32).alias('lives_lost')
            )
            .with_columns(
                (pl.col('lives_start') - pl.col('lives_lost')).alias('lives_end')
            )
        )

        diff_df_filled = pl.concat([diff_df_filled, diff_df_week])

    # add flag for current gw
    diff_df_filled = (
        diff_df_filled
        .with_columns(
            (pl.col('event') == pl.col('event').max()).alias('current_gw')
        )
    )
    
    # add to MongoDB for charting
    result = last_man_standing_collection.delete_many({})
    result = last_man_standing_collection.insert_many(diff_df_filled.to_dicts())


if __name__ == '__main__':
    get_lms(MONGO_URI)