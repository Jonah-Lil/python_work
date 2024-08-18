import requests
import pandas as pd

class FplApi:
    def __init__(self) -> None:
        self.url = "https://fantasy.premierleague.com/api/"
    
    def get_h2h_league(self, league_id):
        query = f"leagues-h2h/{league_id}/standings/"
        response = requests.get(self.url + query)

        return response.json()
    
    def get_general(self):
        query = f"bootstrap-static/"
        response = requests.get(self.url + query)

        return response.json()
    
    def get_manager(self, team_id):
        query = f"entry/{team_id}/"
        response = requests.get(self.url + query)

        return response.json()

    def get_manager_transfers(self, team_id):
        query = f"entry/{team_id}/transfers/"
        response = requests.get(self.url + query)

        return response.json()

    def get_manager_history(self, team_id):
        query = f"entry/{team_id}/history/"
        response = requests.get(self.url + query)

        return response.json()

if __name__ == "__main__":
    fpl = FplApi()
    data = fpl.get_h2h_league(147261)
    current_entrants = data['new_entries']['results']