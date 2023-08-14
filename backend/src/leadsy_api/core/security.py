import hashlib
import os
from datetime import datetime

from fastapi.security import OAuth2PasswordBearer
from jose import jwt
from passlib.context import CryptContext

from leadsy_api.core.config import get_settings

password_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
reusable_oauth_scheme = OAuth2PasswordBearer(
    tokenUrl=f"/api/{get_settings().api_version}/oauth2/token"
)


def generate_hash(plain_text: str) -> str:
    return password_context.hash(plain_text)


def check_password(plain_text: str, password: str) -> bool:
    return password_context.verify(plain_text, password)


def create_access_token(subject: str, *, expires_at: datetime) -> str:
    payload = {"sub": subject, "exp": expires_at}
    encoded = jwt.encode(payload, get_settings().app_key, algorithm="HS256")
    return encoded


def generate_random_password_token() -> str:
    return hashlib.md5(os.urandom(32)).hexdigest()
