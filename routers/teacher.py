from fastapi import APIRouter, Depends, HTTPException

from sqlalchemy.orm import Session

from database import get_db

from models.student import Student
from models.course import Course
from models.teacher import Teacher

from schema.teacher import (
    TeacherCreate,
    TeacherResponse,
)
router = APIRouter(
    prefix="/teachers",
    tags=["Teachers"]
)



@router.post(
    "/",
    response_model=TeacherResponse
)
def create_teacher(
    teacher: TeacherCreate,
    db: Session = Depends(get_db)
):

    existing_teacher = db.query(Teacher).filter(
        Teacher.email == teacher.email
    ).first()

    if existing_teacher:

        raise HTTPException(
            status_code=400,
            detail="Teacher email already exists"
        )

    new_teacher = Teacher(
        name=teacher.name,
        email=teacher.email
    )

    db.add(new_teacher)

    db.commit()

    db.refresh(new_teacher)

    return new_teacher


# =========================
# GET ALL TEACHERS
# =========================

@router.get(
    "/",
    response_model=list[TeacherResponse]
)
def get_teachers(
    db: Session = Depends(get_db)
):

    teachers = db.query(Teacher).all()

    return teachers


# =========================
# GET STUDENTS OF TEACHER
# =========================

@router.get(
    "/{teacher_id}/students"
)
def get_teacher_students(
    teacher_id: int,
    db: Session = Depends(get_db)
):

    teacher = db.query(Teacher).filter(
        Teacher.id == teacher_id
    ).first()

    if not teacher:

        raise HTTPException(
            status_code=404,
            detail="Teacher not found"
        )

    courses = db.query(Course).filter(
        Course.teacher_id == teacher_id
    ).all()

    result = []

    for course in courses:

        students = db.query(Student).filter(
            Student.course_id == course.id
        ).all()

        result.append(
            {
                "course_id": course.id,
                "course": course.name,
                "students": [
                    {
                        "id": student.id,
                        "roll_no": student.roll_no,
                        "name": student.name
                    }
                    for student in students
                ]
            }
        )

    return {
        "teacher_id": teacher.id,
        "teacher": teacher.name,
        "courses": result
    }