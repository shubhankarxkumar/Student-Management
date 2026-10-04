from sqlalchemy import Column, Integer, ForeignKey, String
from sqlalchemy.orm import relationship

from database import Base


class Student(Base):
    __tablename__ = "students"

    id = Column(
        Integer,
        primary_key=True,
        index=True
    )

    roll_no = Column(
        Integer,
        unique=True,
        nullable=False,
        index=True
    )

    name = Column(
        String,
        nullable=False
    )

    course_id = Column(
        Integer,
        ForeignKey("courses.id"),
        nullable=False
    )

    # Student -> Course~git
    course = relationship(
        "Course",
        back_populates="students"
    )

    # Student -> Marks
    marks = relationship(
        "Marks",
        back_populates="student"
    )
