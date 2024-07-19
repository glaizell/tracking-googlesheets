import os
import requests
from datetime import datetime
from dotenv import load_dotenv, find_dotenv
from requests.auth import HTTPBasicAuth


class WorkoutTracker:
    def __init__(self, env_path):
        self.load_env_variables(env_path)
        self.username = os.getenv("USERNAME")
        self.password = os.getenv("PASSWORD")
        self.app_id = os.getenv("APP_ID")
        self.api_key = os.getenv("API_KEY")
        self.sheet_endpoint = os.getenv("SHEET_ENDPOINT")
        self.token = os.getenv("TOKEN")
        self.exercise_endpoint = "https://trackapi.nutritionix.com/v2/natural/exercise"

    def load_env_variables(self, env_path):
        dotenv_path = find_dotenv(env_path)
        if dotenv_path:
            print(f"Found .env file at: {dotenv_path}")
            load_dotenv(dotenv_path)
        else:
            print("Warning: .env file not found!")

    def get_exercise_data(self, miles):
        headers = {
            "x-app-id": self.app_id,
            "x-app-key": self.api_key,
            "x-remote-user-id": "0",
        }
        params = {
            "query": miles,
            "weight_kg": 55,
            "height_cm": 167.64,
            "age": 60,
        }
        response = requests.post(url=self.exercise_endpoint, json=params, headers=headers)
        return response.json()

    def log_exercise(self, data):
        today_date = datetime.now().strftime("%d/%m/%Y")
        now_time = datetime.now().strftime("%X")
        sheety_headers = {
            "Authorization": f"Basic {self.token}",
            "Content-Type": "application/json",
        }
        basic_auth = HTTPBasicAuth(self.username, self.password)
        for exercise in data["exercises"]:
            inputs = {
                "workout": {
                    "date": today_date,
                    "time": now_time,
                    "exercise": exercise["name"].title(),
                    "duration": exercise["duration_min"],
                    "calories": exercise["nf_calories"]
                }
            }
            sheety_response = requests.post(url=self.sheet_endpoint, json=inputs, headers=sheety_headers,
                                            auth=basic_auth)
            print(sheety_response.text)

    def track_workout(self):
        miles = input("How many miles you run?")
        exercise_data = self.get_exercise_data(miles)
        self.log_exercise(exercise_data)


path_to_env = ""
if __name__ == "__main__":
    tracker = WorkoutTracker(path_to_env)
    tracker.track_workout()
