import pandas as pd
from entrant_data import team_ids
from fpl_class_vs import FplApi

def fetch_manager_histories(api: FplApi, team_ids: list) -> pd.DataFrame:
    """Fetches manager history for all team IDs and returns a DataFrame."""
    histories = []
    
    for team_id in team_ids:
        print(f"Fetching history for team ID: {team_id}")
        history = api.get_manager_history(team_id)
        
        # Check if the response contains the expected data
        if 'current' in history:
            for entry in history['current']:
                entry['team_id'] = team_id  # Add team_id to each entry
                histories.append(entry)
        else:
            print(f"No history found for team ID: {team_id}")
    
    return pd.DataFrame(histories)

if __name__ == "__main__":
    fpl = FplApi()
    manager_histories_df = fetch_manager_histories(fpl, team_ids)
    
    # Display or save the DataFrame as needed
    print(manager_histories_df.head())  # Display the first few rows

