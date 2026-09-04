import requests
from ..data_manager import DataManager
from src.constants import SERVER_HTTP, ACCOUNT_DATA_FILE

class AccountManager:
    def __init__(self):
        self.player_id = None
        self.username = None
        self.token = None
        
        self.remeber_me = True
        
        data = DataManager.read(ACCOUNT_DATA_FILE)
        if data:
            self.login(data.get("username"), data.get("password"))

    def is_logged_in(self) -> bool:
        return self.player_id is not None

    def get_player_id(self) -> int | None:
        return self.player_id

    def login(self, username: str, password: str) -> bool:
        if not username or not password:
            return False

        try:
            response = requests.post(
                f"{SERVER_HTTP}/auth/login",
                json={"username": username, "password": password}
            )

            if response.status_code == 200:
                data = response.json()
                self.player_id = data["id"]
                self.username = data["username"]
                self.token = data.get("token")
                
                if self.remeber_me:
                    DataManager.write(ACCOUNT_DATA_FILE, {"username": username, "password": password})
                
                return True

            return False

        except requests.ConnectionError:
            print("Server unreachable")
            return False

    def signup(self, username: str, password: str) -> bool:
        if not username or not password:
            return False

        try:
            response = requests.post(
                f"{SERVER_HTTP}/auth/signup",
                json={"username": username, "password": password}
            )

            if response.status_code == 200:
                data = response.json()
                self.player_id = data["id"]
                self.username = data["username"]
                self.token = data.get("token")
                
                if self.remeber_me:
                    DataManager.write(ACCOUNT_DATA_FILE, {"username": username, "password": password})
                                    
                return True

            return False

        except requests.ConnectionError:
            print("Server unreachable")
            return False

    def logout(self):
        self.player_id = None
        self.username = None
        self.token = None
        
        DataManager.delete(ACCOUNT_DATA_FILE)

account_manager = AccountManager()