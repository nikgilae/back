from fastapi import Depends, HTTPException, Security
from fastapi.security import APIKeyHeader
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from database import get_db
from models.user import User
from services.auth import decode_token

api_key_header = APIKeyHeader(name="Authorization")


async def get_current_user(token: str = Security(api_key_header), db: AsyncSession = Depends(get_db)):
    user_id = decode_token(token)
    if user_id is None:
        raise HTTPException(status_code=401, detail="Недействительный токен")
    result = await db.execute(select(User).where(User.id == user_id))
    user = result.scalar_one_or_none()
    if user is None:
        raise HTTPException(status_code=401, detail="Пользователь не найден")
    return user