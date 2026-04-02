from fastapi import APIRouter, Depends, UploadFile, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from database import get_db
from api.dependencies import get_current_user
from models.user import User
from minio_client import upload_file
import services.task as task_service

router = APIRouter(prefix="/v1/tasks", tags=["Upload"])


@router.post("/{task_id}/upload-avatar")
async def upload_avatar(
    task_id: int,
    file: UploadFile,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    await task_service.get_by_id(db, task_id, current_user.id)

    file_bytes = await file.read()
    filename = f"task_{task_id}_{file.filename}"

    url = await upload_file(file_bytes, filename)
    return {"url": url}