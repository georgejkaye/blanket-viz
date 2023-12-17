from dataclasses import dataclass
from datetime import date, datetime, timedelta
from decimal import Decimal
from typing import Annotated, Optional
from api.database import Observation, insert_observation, select_observations
from fastapi import Depends, FastAPI, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm

from api.auth import (
    ACCESS_TOKEN_EXPIRE_MINUTES,
    authenticate_user,
    create_access_token,
    get_env_variable,
    validate_token,
)


app = FastAPI(
    title="Temperature blanket API",
    summary="API for interacting with the temperature blanket",
    version="1.0.0",
    contact={
        "name": "George Kaye",
        "email": "georgejkaye@gmail.com",
        "url": "https://georgejkaye.com",
    },
    license_info={
        "name": "GNU General Public License v3.0",
        "url": "https://www.gnu.org/licenses/gpl-3.0.en.html",
    },
)


@app.post("/token", summary="Get an auth token")
async def login(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
):
    # Check the username and password
    user = authenticate_user(form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    # Create an access token
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(data={}, expires_delta=access_token_expires)
    return {"access_token": access_token, "token_type": "bearer"}


@app.post("/observation", summary="Submit a new observation")
async def post_observation(
    token: Annotated[Optional[str], Depends(validate_token)],
    actual_datetime: Optional[datetime],
    row_date: date,
    temperature: Decimal,
    is_day: bool,
) -> None:
    observation = Observation(actual_datetime, temperature, row_date, is_day)
    insert_observation(observation)


@app.get("/observations", summary="Get observations")
async def get_commits(
    start: Optional[datetime] = None,
    end: Optional[datetime] = None,
) -> list[Observation]:
    return select_observations(start=start, end=end)


import uvicorn


def start():
    if get_env_variable("API_ENV") == "prod":
        reload = False
    elif get_env_variable("API_ENV") == "dev":
        reload = True
    else:
        print("Invalid environment set")
        exit(1)
    uvicorn.run(
        "api.main:app",
        host="0.0.0.0",
        port=int(get_env_variable("API_PORT")),
        reload=reload,
    )


if __name__ == "__main__":
    start()
