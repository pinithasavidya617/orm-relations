from sqlalchemy.ext.asyncio import AsyncSession

from db_models import Teacher, TeacherProfile
from response_models import TeacherCreate, TeacherResponse


class TeacherRepository:

    def __init__(self, db: AsyncSession):
        self.db = db

    async def create(self, data: TeacherCreate) -> Teacher:
        teacher = Teacher(name=data.name, email=data.email)

        if data.profile:
            teacher.profile = TeacherProfile(**data.profile.model_dump())

        self.db.add(teacher)
        await self.db.commit()
        await self.db.refresh(teacher)
        return teacher