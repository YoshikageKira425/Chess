import os
import json

class DataManager:
    
    @staticmethod
    def read(filename: str) -> dict | None:
        try:
            with open(f"data/{filename}.json", "r") as f:
                return json.load(f)
        except:
            return None
        
    @staticmethod
    def write(filename: str, data: dict):
        os.makedirs("data", exist_ok=True)
        with open(f"data/{filename}.json", "w") as f:
            json.dump(data, f)
            
    @staticmethod
    def delete(filename: str):
        try:
            os.remove(f"data/{filename}.json")
        except FileNotFoundError:
            pass