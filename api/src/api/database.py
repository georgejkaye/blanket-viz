from dataclasses import dataclass
from datetime import date, datetime
from decimal import Decimal
from typing import Any, Optional
from fastapi import HTTPException
import os

import psycopg2

from api.auth import get_env_variable


def read_secret(file: str) -> Optional[str]:
    if os.path.isfile(file):
        with open(file) as f:
            value = f.readline().replace("\n", "")
        return value
    return None


def connect() -> tuple[Any, Any]:
    conn = psycopg2.connect(
        dbname=get_env_variable("DB_NAME"),
        user=get_env_variable("DB_USER"),
        password=read_secret(get_env_variable("DB_PASSWORD")),
        host=get_env_variable("DB_HOST"),
    )
    cur = conn.cursor()
    return (conn, cur)


def disconnect(conn: Any, cur: Any) -> None:
    conn.close()
    cur.close()


@dataclass
class Observation:
    actual_datetime: Optional[datetime]
    temperature: Decimal
    row_date: date
    is_day: bool


def insert_observation(observation: Observation) -> None:
    (conn, cur) = connect()
    statement = """
        INSERT INTO observation(actual_datetime, observation_temp, row_date, is_day)
        VALUES (%(dt)s, %(temp)s, %(date)s, %(is_day)s)
    """
    try:
        cur.execute(
            statement,
            {
                "dt": observation.actual_datetime,
                "temp": observation.temperature,
                "date": observation.row_date,
                "is_day": observation.is_day,
            },
        )
        conn.commit()
        disconnect(conn, cur)
    except psycopg2.errors.UniqueViolation as e:
        raise HTTPException(status_code=400, detail="Observation already exists")


def select_observations(
    start: Optional[date] = None, end: Optional[date] = None
) -> list[Observation]:
    (conn, cur) = connect()
    conditions = []
    if start is not None:
        conditions.append("row_date >= %(start)s")
    if end is not None:
        conditions.append("row_date <= %(end)s")
    if len(conditions) == 0:
        conditions_string = ""
    else:
        conditions_string = f"WHERE {' AND '.join(conditions)}"
    statement = f"""
        SELECT actual_datetime, observation_temp, row_date, is_day FROM observation
        {conditions_string}
        ORDER BY row_date DESC, is_day ASC
    """
    cur.execute(statement)
    rows = cur.fetchall()
    observation_objects = list(map(lambda b: Observation(b[0], b[1], b[2], b[3]), rows))
    conn.close()
    return observation_objects
