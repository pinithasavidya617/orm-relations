from datetime import datetime
from typing import Optional

from sqlalchemy import String, func, Text, ForeignKey
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column


class Base(DeclarativeBase):
    pass

class Teacher(Base):
    __tablename__ = "teachers"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    email : Mapped[str] = mapped_column(String(255), nullable=False)
    created_at : Mapped[datetime] = mapped_column(server_default=func.now(), default=datetime.now())

class TeacherProfile(Base):
    __tablename__ = "teacher_profiles"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    teacher_id: Mapped[int] = mapped_column(ForeignKey("teacher.id", ondelete="CASCADE"))
    qualifications : Mapped[Optional[str]] = mapped_column(String(300), nullable=True)
    department : Mapped[Optional[str]] = mapped_column(String(250), nullable=True)
    office_number : Mapped[Optional[str]] = mapped_column(String(30), nullable=True)
    bio : Mapped[Text] = mapped_column(nullable=True)

