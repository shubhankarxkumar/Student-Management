from sqlalchemy import Column, Integer, ForeignKey, UniqueConstraint
from sqlalchemy.orm import relationship

from database import Base


class Marks(Base):
    __tablename__ = "marks"

    id = Column(
        Integer,
        primary_key=True,
        index=True
    )

    student_id = Column(
        Integer,
        ForeignKey("students.id"),
        nullable=False
    )

    course_id = Column(
        Integer,
        ForeignKey("courses.id"),
        nullable=False
    )

    marks = Column(
        Integer,
        nullable=False
    )

    # Marks -> Student
    student = relationship(
        "Student",
        back_populates="marks"
    )

    # Marks -> Course
    course = relationship(
        "Course",
        back_populates="marks"
    )

    __table_args__ = (
        UniqueConstraint(
            "student_id",
            "course_id",
            name="unique_student_course_marks"
        ),
    )
