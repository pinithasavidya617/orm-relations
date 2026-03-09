from typing import List

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

@router.get("/{teacher_id}", response_model=TeacherResponse, status_code=status.HTTP_200_OK)
async def get_teacher_by_id(teacher_id: int, db: AsyncSession = Depends(get_db)):
    teacher_repo = TeacherRepository(db)
    teacher = await teacher_repo.get_by_id(teacher_id)
    return teacher

@router.get("/", response_model=List[TeacherResponse], status_code=status.HTTP_200_OK)
async def get_all_teachers(offset:int = 0,
                           limit: int = 20,
                           db: AsyncSession = Depends(get_db)):
    teacher_repo = TeacherRepository(db)
    teachers = await teacher_repo.get_all(offset, limit)
    return teachers

@router.get("/email/{email}", response_model=TeacherResponse, status_code=status.HTTP_200_OK)
async def get_teacher_by_email(email: str, db: AsyncSession = Depends(get_db)):
    teacher_repo = TeacherRepository(db)
    teacher = await teacher_repo.teacher_get_by_email(email)
    return teacher