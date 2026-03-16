from datetime import datetime
from typing import Optional, List

from sqlalchemy import String, func, Text, ForeignKey, Integer, Table, Column
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship


class Base(DeclarativeBase):
    pass

# M to M relation only create pure relationship table not a common type table
enrollment = Table(
    'enrollments',
    Base.metadata,

    Column('student_id',
           Integer,
           ForeignKey('students.id' , ondelete='CASCADE'),
           primary_key=True),

    Column('course_id',
           Integer,
           ForeignKey('courses.id' , ondelete='CASCADE'),
           primary_key=True),
)


class Teacher(Base):
    __tablename__ = "teachers"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    email : Mapped[str] = mapped_column(String(255), nullable=False)
    created_at : Mapped[datetime] = mapped_column(server_default=func.now(), default=datetime.now())

    profile: Mapped[Optional["TeacherProfile"]] = relationship(
        back_populates="teacher" ,
        uselist=False,
        cascade="all, delete-orphan",
        lazy="joined"
    ) #uselist refers 1 to 1 relationship
    #lazy = joined mean, set loading to eager loading

    courses: Mapped[List["Courses"]] = relationship(
        back_populates="teacher",
        cascade="all, delete-orphan",
        lazy="selectin"   #in queries
    )

class Courses(Base):
    __tablename__ = "courses"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    teacher_id: Mapped[int] = mapped_column(
        ForeignKey("teachers.id", ondelete="CASCADE"),
    )
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    code: Mapped[str] = mapped_column(String(255), nullable=False)
    description: Mapped[str] = mapped_column(String(255), nullable=False)
    credits: Mapped[Optional[int]] = mapped_column(default=5)
    is_active: Mapped[bool] = mapped_column(default=True)
    created_at: Mapped[datetime] = mapped_column(server_default=func.now(), default=datetime.now())

    teacher: Mapped["Teacher"] = relationship(
        back_populates="courses", )


class TeacherProfile(Base):
    __tablename__ = "teacher_profiles"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    teacher_id: Mapped[int] = mapped_column(ForeignKey("teachers.id", ondelete="CASCADE"))
    qualifications: Mapped[Optional[str]] = mapped_column(String(300), nullable=True)
    department: Mapped[Optional[str]] = mapped_column(String(250), nullable=True)
    office_number: Mapped[Optional[str]] = mapped_column(String(30), nullable=True)
    bio: Mapped[Optional[str]] = mapped_column(Text)
    teacher: Mapped[Optional[Teacher]] = relationship(back_populates="profile")


class Student(Base):
    __tablename__ = 'students'

    id : Mapped[int] = mapped_column(primary_key=True , index=True )
    name : Mapped[str] = mapped_column(String(300), nullable=False)
    email : Mapped[str] = mapped_column(String(255), nullable=False)
    enrollment_year : Mapped[int]

    courses : Mapped[List["Course"]] = relationship(
        secondary=enrollment,
        back_populates="student",
        lazy="selectin",
    )