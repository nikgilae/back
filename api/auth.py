from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from database import get_db
from schemas.user import UserRegister, UserLogin, TokenResponse
import services.auth as auth_service

router = APIRouter(prefix="/auth", tags=["Auth"])


@router.post("/register", status_code=201)
async def register(data: UserRegister, db: AsyncSession = Depends(get_db)):
    user = await auth_service.register(db, data.username, data.password)
    if user is None:
        raise HTTPException(status_code=400, detail="Пользователь с таким именем уже существует")
    return {"message": "Пользователь успешно зарегистрирован"}


@router.post("/login", response_model=TokenResponse)
async def login(data: UserLogin, db: AsyncSession = Depends(get_db)):
    token = await auth_service.login(db, data.username, data.password)
    if token is None:
        raise HTTPException(status_code=401, detail="Неверный логин или пароль")
    return {"access_token": token}