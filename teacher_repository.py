from fastapi import HTTPException
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import joinedload, selectinload

from db_models import Teacher, TeacherProfile
from response_models import TeacherCreate, TeacherResponse


class TeacherRepository:

    def __init__(self, db: AsyncSession):
        self.db = db

    async def create(self, data: TeacherCreate) -> Teacher:
        teacher = Teacher(name=data.name, email=data.email)

        if data.profile:
            teacher.profile = TeacherProfile(**data.profile.model_dump())

        try:
            self.db.add(teacher)
            await self.db.commit()
            await self.db.refresh(teacher)
            return teacher

        except IntegrityError:
            await self.db.rollback()
            raise HTTPException(
                status_code=409,
                detail=f"A teacher with email '{data.email}' already exists."
            )

    async def get_by_id(self, teacher_id: int) -> Teacher | None:
        query = (
            select(Teacher)
            .where(Teacher.id == teacher_id)
            .options(joinedload(Teacher.profile),
                     selectinload(Teacher.courses))
        )

        result = await self.db.execute(query)
        return result.unique().scalars().first()