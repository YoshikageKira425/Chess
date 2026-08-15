import requests
from src.constants import SERVER_URL

class AccountManager:
    def __init__(self):
        self.player_id = None
        self.username = None
        self.token = None

    def is_logged_in(self) -> bool:
        return self.player_id is not None

    def get_player_id(self) -> int | None:
        return self.player_id

    def login(self, username: str, password: str) -> bool:
        if not username or not password:
            return False

        try:
            response = requests.post(
                f"{SERVER_URL}/auth/login",
                json={"username": username, "password": password}
            )

            if response.status_code == 200:
                data = response.json()
                self.player_id = data["id"]
                self.username = data["username"]
                self.token = data.get("token")
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
                f"{SERVER_URL}/auth/signup",
                json={"username": username, "password": password}
            )

            if response.status_code == 200:
                data = response.json()
                self.player_id = data["id"]
                self.username = data["username"]
                self.token = data.get("token")
                return True

            return False

        except requests.ConnectionError:
            print("Server unreachable")
            return False

    def logout(self):
        self.player_id = None
        self.username = None
        self.token = None
