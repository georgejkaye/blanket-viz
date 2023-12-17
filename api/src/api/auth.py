from datetime import timedelta, datetime
import os
from typing import Annotated, Optional
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from passlib.context import CryptContext
from pydantic import BaseModel


def get_env_variable(name: str) -> str:
    var = os.getenv(name)
    if var:
        return var
    else:
        print(f"Environment variable {name} not set")
        exit(1)


def get_secret(name: str) -> str:
    file = get_env_variable(name)
    if not os.path.isfile(file):
        raise FileNotFoundError(f"Secret file {file} not found")
    with open(file, "r") as f:
        secret = f.read().replace("\n", "")
    return secret


ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/token", auto_error=False)


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    username: str | None = None


def verify_password(plain_password, hashed_password) -> bool:
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password) -> str:
    hashed_password = pwd_context.hash(password)
    return hashed_password


def authenticate_user(username: str, password: str) -> bool:
    valid_user = get_env_variable("ADMIN_USER")
    hashed_password = get_secret("ADMIN_PASSWORD_HASHED")
    if not (valid_user == username):
        print("Invalid user")
        return False
    if not verify_password(password, hashed_password):
        return False
    return True


def create_access_token(data: dict, expires_delta: timedelta | None = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, get_secret("SECRET_KEY"), algorithm=ALGORITHM)
    return encoded_jwt


async def validate_token(
    token: Annotated[Optional[str], Depends(oauth2_scheme)]
) -> Optional[bool]:
    if token:
        credentials_exception = HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
        try:
            jwt.decode(token, get_secret("SECRET_KEY"), algorithms=[ALGORITHM])
            return True
        except JWTError:
            raise credentials_exception
    return None
