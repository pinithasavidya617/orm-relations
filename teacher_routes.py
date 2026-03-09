from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status

from database_config import get_db
from response_models import TeacherResponse, TeacherCreate
from teacher_repository import TeacherRepository

router = APIRouter(prefix="/teachers", tags=["Teacher Endpoints"])

@router.post("/", response_model=TeacherResponse, status_code=status.HTTP_201_CREATED)
async def create_user(teacher_create : TeacherCreate, db: AsyncSession = Depends(get_db)):

    teacher_repo = TeacherRepository(db)
    teacher = await teacher_repo.create(data=teacher_create)
    return teacher