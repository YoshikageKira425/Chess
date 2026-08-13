import requests
import json
import os
from src.constants import SERVER_URL

class AccountManager:
    def __init__(self):
        self.player_id = None
        self.username = None
        self.token = None

        saved = self._read()
        if saved:
            self.login(saved["username"], saved["password"])

    def _read(self) -> dict | None:
        try:
            with open("data/player_data.json") as f:
                return json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            return None

    def _save(self, username: str, password: str):
        os.makedirs("data", exist_ok=True)
        with open("data/player_data.json", "w") as f:
            json.dump({"username": username, "password": password}, f)

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
                self._save(username, password)
                return True

            return False

        except requests.ConnectionError:
            print("Server unreachable")
            return False

    def logout(self):
        self.player_id = None
        self.username = None
        self.token = None

        try:
            os.remove("data/player_data.json")
        except FileNotFoundError:
            pass