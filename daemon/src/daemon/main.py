from datetime import time, date, datetime, timedelta
import sys
from typing import Optional
from daemon.observe import (
    get_observation_from_range,
    get_observations,
    post_observation,
)
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


def make_observation(
    station_id: int,
    start_time: datetime,
    end_time: datetime,
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
        observations = get_observations(station_id)
        obs = get_observation_from_range(observations, start_time, end_time, greatest)
        post_observation(endpoint, token, obs, date, greatest)


def make_observation_from_variables(
    station_id_var: str, start_time_var: str, end_time_var: str, greatest: bool
):
    station_id = int(get_env_variable(station_id_var))
    today = datetime.today().date()
    start_time = get_time_from_env(start_time_var)
    end_time = get_time_from_env(end_time_var)
    if start_time <= end_time:
        start_date = today
        end_date = today
    else:
        start_date = today - timedelta(days=1)
        end_date = today
    start_datetime = datetime.combine(start_date, start_time)
    end_datetime = datetime.combine(end_date, end_time)
    make_observation(station_id, start_datetime, end_datetime, start_date, greatest)
