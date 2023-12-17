from datetime import time, date, datetime
import sys
from typing import Optional
from daemon.observe import get_observation_from_range, post_observation
from daemon.utils import get_env_variable, get_secret
import requests


def get_token(endpoint: str, user: str, password: str) -> Optional[str]:
    url = f"{endpoint}/token"
    headers = {
        "accept": "application/json",
        "Content-Type": "application/x-www-form-urlencoded",
    }
    data = {"username": user, "password": password}
    response = requests.post(url, headers=headers, data=data)
    if not response.status_code == 200:
        print("Could not get token")
        return None
    else:
        token = response.json()["access_token"]
        return token


def request_update(endpoint: str, token: str):
    url = f"{endpoint}/breaks/update"
    headers = {"accept": "application/json", "Authorization": f"Bearer {token}"}
    requests.post(url, headers=headers)


def get_time_from_env(name: str) -> time:
    time_str = get_env_variable(name)
    return datetime.strptime(time_str, "%H:%M").time()


def main(
    station_id: int,
    start_time: time,
    end_time: time,
    date: date,
    greatest: bool,
):
    endpoint = get_env_variable("API_ENDPOINT")
    token = get_token(
        endpoint,
        get_env_variable("API_USER"),
        get_secret("API_PASSWORD"),
    )
    if token:
        obs = get_observation_from_range(station_id, start_time, end_time, greatest)
        post_observation(endpoint, token, obs, date, greatest)
