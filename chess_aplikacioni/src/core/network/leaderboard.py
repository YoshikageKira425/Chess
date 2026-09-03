import requests
from src.constants import SERVER_HTTP

class Leaderboard:
    
    @staticmethod
    def gettin_top_ten():
        try:
            response = requests.get(f"{SERVER_HTTP}/leaderboard")
            
            if response.status_code == 200:
                data = response.json()
                return data
                
            return None
        except requests.ConnectionError:
            print("Server unreachable")
            return None
    
    @staticmethod
    def get_user_elo(user_id: int):
        if not user_id:
            return
        
        try:
            response = requests.get(f"{SERVER_HTTP}/leaderboard/elo/{user_id}")
            
            if response.status_code == 200:
                data = response.json()
                return data.get("elo")
                
            return None
        except requests.ConnectionError:
            print("Server unreachable")
            return None
            