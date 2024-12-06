from typing import Any
import jwt
from datetime import datetime, timedelta, timezone
from passlib.context import CryptContext

from app import config

bcrypt_context = CryptContext(schemes=['bcrypt'], deprecated="auto")

def hashed_pass(password: str) -> str:
    return bcrypt_context.hash(password)

def verify_pass(password: str, hashed: str) -> bool:
    return bcrypt_context.verify(password, hashed)

def create_access_token(data: dict | Any):
    expire = datetime.now(timezone.utc) + timedelta(config.setting.ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode = data.copy()
    to_encode.update({'exp': expire})
    encoded_jwt = jwt.encode(to_encode, config.setting.JWT_KEY, algorithm=config.setting.ALGORITHM)
    return encoded_jwt