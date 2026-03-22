from fastapi import Depends, HTTPException
from fastapi.security import APIKeyHeader
from sqlalchemy.orm import Session

from database import get_db
from models.user import User
from services.auth import decode_token

api_key_scheme = APIKeyHeader(name="Authorization")


def get_current_user(token: str = Depends(api_key_scheme), db: Session = Depends(get_db)):
    user_id = decode_token(token)
    if user_id is None:
        raise HTTPException(status_code=401, detail="Недействительный токен")
    user = db.query(User).filter(User.id == user_id).first()
    if user is None:
        raise HTTPException(status_code=401, detail="Пользователь не найден")
    return user