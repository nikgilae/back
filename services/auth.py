from datetime import datetime, timedelta, UTC
from jose import jwt
from passlib.context import CryptContext
from sqlalchemy.orm import Session

import repositories.user as user_repo

SECRET_KEY = "super-secret-key-change-in-production"
ALGORITHM = "HS256"
TOKEN_EXPIRE_MINUTES = 60

pwd_context = CryptContext(schemes=["bcrypt"])


def hash_password(password: str) -> str:
    return pwd_context.hash(password)


def verify_password(plain: str, hashed: str) -> bool:
    return pwd_context.verify(plain, hashed)


def create_token(user_id: int) -> str:
    expire = datetime.now(UTC) + timedelta(minutes=TOKEN_EXPIRE_MINUTES)
    payload = {"sub": str(user_id), "exp": expire}
    return jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)


def decode_token(token: str) -> int | None:
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return int(payload["sub"])
    except Exception:
        return None


def register(db: Session, username: str, password: str):
    existing = user_repo.get_by_username(db, username)
    if existing:
        return None
    hashed = hash_password(password)
    return user_repo.create(db, username, hashed)


def login(db: Session, username: str, password: str) -> str | None:
    user = user_repo.get_by_username(db, username)
    if not user:
        return None
    if not verify_password(password, user.hashed_password):
        return None
    return create_token(user.id)