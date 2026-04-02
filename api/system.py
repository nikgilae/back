from fastapi import APIRouter
from sqlalchemy import text
from database import SessionLocal
from minio_client import check_minio

router = APIRouter(tags=["System"])


@router.get("/health")
async def health():
    db_ok = False
    try:
        async with SessionLocal() as db:
            await db.execute(text("SELECT 1"))
            db_ok = True
    except Exception:
        pass

    minio_ok = await check_minio()

    return {
        "db": "ok" if db_ok else "error",
        "minio": "ok" if minio_ok else "error",
    }


@router.get("/info")
async def info():
    return {
        "version": "1.0.0",
        "environment": "development",
    }