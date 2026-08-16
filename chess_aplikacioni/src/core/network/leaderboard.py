import requests
from src.constants import SERVER_URL

class Leaderboard:
    
    @staticmethod
    def gettin_top_ten():
        try:
            response = requests.get(f"{SERVER_URL}/leaderboard")
            
            if response.status_code == 200:
                data = response.json()
                return data
                
            return None
        except requests.ConnectionError:
            print("Server unreachable")
            return None
        
            