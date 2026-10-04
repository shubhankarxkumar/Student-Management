from fastapi import APIRouter, Depends, HTTPException

from sqlalchemy.orm import Session

from database import get_db

from models.student import Student
from models.course import Course

from schema.student import (
    StudentCreate,
    StudentResponse,
    StudentCourseUpdate
)


router = APIRouter(
    prefix="/students",
    tags=["Students"]
)


# =========================
# CREATE STUDENT
# =========================

@router.post(
    "/",
    response_model=StudentResponse
)
def create_student(
    student: StudentCreate,
    db: Session = Depends(get_db)
):

    course = db.query(Course).filter(
        Course.id == student.course_id
    ).first()

    if not course:
        raise HTTPException(
            status_code=404,
            detail="Course not found"
        )

    existing_student = db.query(Student).filter(
        Student.roll_no == student.roll_no
    ).first()

    if existing_student:
        raise HTTPException(
            status_code=400,
            detail="Roll number already exists"
        )

    new_student = Student(
        roll_no=student.roll_no,
        name=student.name,
        course_id=student.course_id
    )

    db.add(new_student)

    db.commit()

    db.refresh(new_student)

    return new_student


# =========================
# GET ALL STUDENTS
# =========================

@router.get(
    "/",
    response_model=list[StudentResponse]
)
def get_students(
    db: Session = Depends(get_db)
):

    students = db.query(Student).all()

    return students


# =========================
# GET SINGLE STUDENT
# =========================

@router.get(
    "/{student_id}",
    response_model=StudentResponse
)
def get_student(
    student_id: int,
    db: Session = Depends(get_db)
):

    student = db.query(Student).filter(
        Student.id == student_id
    ).first()

    if not student:

        raise HTTPException(
            status_code=404,
            detail="Student not found"
        )

    return student


# =========================
# CHANGE COURSE
# =========================

@router.put(
    "/{student_id}/course",
    response_model=StudentResponse
)
def change_course(
    student_id: int,
    data: StudentCourseUpdate,
    db: Session = Depends(get_db)
):

    student = db.query(Student).filter(
        Student.id == student_id
    ).first()

    if not student:

        raise HTTPException(
            status_code=404,
            detail="Student not found"
        )

    course = db.query(Course).filter(
        Course.id == data.course_id
    ).first()

    if not course:

        raise HTTPException(
            status_code=404,
            detail="Course not found"
        )

    student.course_id = data.course_id

    db.commit()

    db.refresh(student)

    return student