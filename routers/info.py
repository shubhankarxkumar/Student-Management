from fastapi import APIRouter, Depends, HTTPException

from sqlalchemy.orm import Session

from database import get_db

from models.course import Course
from models.teacher import Teacher


router = APIRouter(
    prefix="/info",
    tags=["Info"]
)


@router.get("/")
def get_info(
    db: Session = Depends(get_db)
):

    teachers = db.query(Teacher).all()

    courses = db.query(Course).all()

    return {
        "teachers": [
            {
                "id": teacher.id,
                "name": teacher.name,
                "email": teacher.email
            }
            for teacher in teachers
        ],

        "courses": [
            {
                "id": course.id,
                "name": course.name,
                "teacher": course.teacher.name
            }
            for course in courses
        ]
    }