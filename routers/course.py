from fastapi import APIRouter, Depends, HTTPException

from sqlalchemy.orm import Session

from database import get_db

from models.marks import Marks
from models.student import Student
from models.course import Course
from models.teacher import Teacher

from schema.course import CourseResponse, CourseCreate

router = APIRouter(
    prefix="/courses",
    tags=["Courses"]
)


# =========================
# CREATE COURSE
# =========================

@router.post(
    "/",
    response_model=CourseResponse
)
def create_course(
    course: CourseCreate,
    db: Session = Depends(get_db)
):

    teacher = db.query(Teacher).filter(
        Teacher.id == course.teacher_id
    ).first()

    if not teacher:

        raise HTTPException(
            status_code=404,
            detail="Teacher not found"
        )

    existing_course = db.query(Course).filter(
        Course.name == course.name
    ).first()

    if existing_course:

        raise HTTPException(
            status_code=400,
            detail="Course already exists"
        )

    new_course = Course(
        name=course.name,
        teacher_id=course.teacher_id
    )

    db.add(new_course)

    db.commit()

    db.refresh(new_course)

    return new_course


# =========================
# GET ALL COURSES
# =========================

@router.get(
    "/",
    response_model=list[CourseResponse]
)
def get_courses(
    db: Session = Depends(get_db)
):

    return db.query(Course).all()


# =========================
# GET COURSE INFORMATION
# =========================

@router.get(
    "/{course_id}"
)
def get_course(
    course_id: int,
    db: Session = Depends(get_db)
):

    course = db.query(Course).filter(
        Course.id == course_id
    ).first()

    if not course:

        raise HTTPException(
            status_code=404,
            detail="Course not found"
        )

    students = db.query(Student).filter(
        Student.course_id == course_id
    ).all()

    return {
        "course_id": course.id,
        "course": course.name,
        "teacher": {
            "id": course.teacher.id,
            "name": course.teacher.name,
            "email": course.teacher.email
        },
        "students": [
            {
                "id": student.id,
                "roll_no": student.roll_no,
                "name": student.name
            }
            for student in students
        ]
    }


# =========================
# GET COURSE MARKS
# =========================

@router.get(
    "/{course_id}/marks"
)
def get_course_marks(
    course_id: int,
    db: Session = Depends(get_db)
):

    course = db.query(Course).filter(
        Course.id == course_id
    ).first()

    if not course:

        raise HTTPException(
            status_code=404,
            detail="Course not found"
        )

    marks_records = db.query(Marks).filter(
        Marks.course_id == course_id
    ).all()

    return {
        "course": course.name,
        "teacher": course.teacher.name,
        "students": [
            {
                "student_id": record.student.id,
                "roll_no": record.student.roll_no,
                "name": record.student.name,
                "marks": record.marks
            }
            for record in marks_records
        ]
    }