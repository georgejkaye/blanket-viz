from datetime import date, datetime, time, timedelta
import json
import sys
from daemon.main import get_token

from daemon.observe import Observation, get_observation_from_range, post_observation
from daemon.utils import get_env_variable


# Parsing data from https://www.visualcrossing.com
def import_from_file(file: str) -> list[Observation]:
    with open(file, "r") as f:
        data = json.load(f)
    observations = []
    for day in data["days"]:
        current_date = datetime.fromisoformat(day["datetime"]).date()
        for hour in day["hours"]:
            current_time = datetime.strptime(hour["datetime"], "%H:%M:%S").time()
            current_datetime = datetime.combine(current_date, current_time)
            current_temp = hour["temp"]
            current_obs = Observation(current_datetime, current_temp)
            observations.append(current_obs)
    return observations


def get_observation_for_day(
    observations: list[Observation],
    current_date: date,
    start_time: time,
    end_time: time,
    greatest: bool,
) -> Observation:
    if start_time <= end_time:
        current_start_date = current_date
        current_end_date = current_date
    else:
        current_start_date = current_date
        current_end_date = current_date + timedelta(days=1)
    start_datetime = datetime.combine(current_start_date, start_time)
    end_datetime = datetime.combine(current_end_date, end_time)
    obs = get_observation_from_range(
        observations, start_datetime, end_datetime, greatest
    )
    return obs


def find_and_post_observation(
    token: str,
    endpoint: str,
    observations: list[Observation],
    current_date: date,
    start_time: time,
    end_time: time,
    greatest: bool,
):
    obs = get_observation_for_day(
        observations, current_date, start_time, end_time, greatest
    )
    post_observation(endpoint, token, obs, current_date, greatest)


if __name__ == "__main__":
    file = sys.argv[1]
    start_date = datetime.fromisoformat(sys.argv[2]).date()
    end_date = datetime.fromisoformat(sys.argv[3]).date()
    day_start = datetime.strptime(sys.argv[4], "%H:%M").time()
    day_end = datetime.strptime(sys.argv[5], "%H:%M").time()
    greatest = bool(sys.argv[6])
    observations = import_from_file(file)
    number_of_days = range((end_date - start_date).days + 1)
    endpoint = sys.argv[7]
    token = get_token(endpoint, sys.argv[8], sys.argv[9])
    if token:
        for delta in number_of_days:
            current_date = start_date + timedelta(days=delta)
            find_and_post_observation(
                token,
                endpoint,
                observations,
                current_date,
                day_start,
                day_end,
                greatest,
            )
    else:
        raise RuntimeError("Could not get token")
