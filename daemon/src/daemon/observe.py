from dataclasses import dataclass
from datetime import date, datetime, time, timedelta
from daemon.utils import get_secret
import requests


base_endpoint = "http://datapoint.metoffice.gov.uk/public/data/val/wxobs/all/json/"


def get_obs_url(id: int, key: str) -> str:
    return f"{base_endpoint}/{id}?res=hourly&key={key}"


@dataclass
class Observation:
    obs_datetime: datetime
    obs_temp: float


def data_to_observation(period: date, obs: dict) -> Observation:
    period_offset = int(obs["$"])
    obs_datetime = datetime.combine(period, time()) + timedelta(minutes=period_offset)
    obs_temp = float(obs["T"])
    return Observation(obs_datetime, obs_temp)


def get_period_date(period: str) -> date:
    return date.fromisoformat(period[:-1])


def get_observations(station_id: int) -> list[Observation]:
    key = get_secret("METOFFICE_SECRET")
    url = get_obs_url(station_id, key)
    res = requests.get(url)
    json = res.json()
    periods = json["SiteRep"]["DV"]["Location"]["Period"]
    observations = []
    for period in periods:
        period_date = get_period_date(period["value"])
        for obs in period["Rep"]:
            obs_object = data_to_observation(period_date, obs)
            observations.append(obs_object)
    return observations


def get_observation_from_range(
    observations: list[Observation],
    start_datetime: datetime,
    end_datetime: datetime,
    greatest: bool,
) -> Observation:
    in_range = False
    current_obs = None
    sorted_observations = sorted(observations, key=lambda obs: obs.obs_datetime)
    # If the start time is greater than the end time, we need to cross
    # midnight before checking for the end time
    for obs in sorted_observations:
        obs_datetime = obs.obs_datetime
        if start_datetime <= obs_datetime:
            in_range = False
        elif end_datetime <= obs_datetime:
            in_range = True
            break
        if in_range:
            if current_obs is None:
                current_obs = obs
            else:
                if (greatest and obs.obs_temp > current_obs.obs_temp) or (
                    not greatest and obs.obs_temp < current_obs.obs_temp
                ):
                    current_obs = obs
    if current_obs is None:
        raise RuntimeError("No temperatures found")
    return current_obs


def post_observation(
    endpoint: str, token: str, obs: Observation, row_date: date, is_day: bool
):
    url = f"{endpoint}/observation"
    headers = {"accept": "application/json", "Authorization": f"Bearer {token}"}
    params = {
        "actual_datetime": obs.obs_datetime,
        "row_date": row_date,
        "temperature": obs.obs_temp,
        "is_day": is_day,
    }
    requests.post(url, headers=headers, params=params)
