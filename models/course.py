from sqlalchemy import Column, Integer, ForeignKey, String
from sqlalchemy.orm import relationship

from database import Base


class Course(Base):
    __tablename__ = "courses"

    id = Column(
        Integer,
        primary_key=True,
        index=True
    )

    name = Column(
        String,
        unique=True,
        nullable=False
    )

    teacher_id = Column(
        Integer,
        ForeignKey("teachers.id"),
        nullable=False
    )

    # Course -> Teacher
    teacher = relationship(
        "Teacher",
        back_populates="courses"
    )

    # Course -> Students
    students = relationship(
        "Student",
        back_populates="course"
    )

    # Course -> Marks
    marks = relationship(
        "Marks",
        back_populates="course"
    )
