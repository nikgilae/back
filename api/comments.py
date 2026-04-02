from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List

from database import get_db
from schemas.comment import CommentCreate, CommentResponse
from api.dependencies import get_current_user
from models.user import User
import services.comment as comment_service

router = APIRouter(prefix="/v1/tasks", tags=["Comments"])


@router.post("/{task_id}/comments", response_model=CommentResponse, status_code=201)
async def create_comment(
    task_id: int,
    data: CommentCreate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return await comment_service.create(db, data, task_id, current_user.id, current_user.id)


@router.get("/{task_id}/comments", response_model=List[CommentResponse])
async def get_comments(
    task_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return await comment_service.get_all(db, task_id, current_user.id)