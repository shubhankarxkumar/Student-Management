from fastapi import APIRouter, Depends, HTTPException

from sqlalchemy.orm import Session

from database import get_db

from models.marks import Marks
from models.student import Student
from models.course import Course

from schema.marks import (
    MarksCreate,
    MarksUpdate,
    BulkMarksUpdate,
    MarksCreateByRoll,
    MarksResponse
)

router = APIRouter(
    prefix="/marks",
    tags=["Marks"]
)



@router.post("/")
def create_marks(
    data: MarksCreate,
    db: Session = Depends(get_db)
):

    student = db.query(Student).filter(
        Student.id == data.student_id
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

    # Important business rule
    if student.course_id != data.course_id:

        raise HTTPException(
            status_code=400,
            detail="Student is not enrolled in this course"
        )

    existing_marks = db.query(Marks).filter(
        Marks.student_id == data.student_id,
        Marks.course_id == data.course_id
    ).first()

    if existing_marks:

        raise HTTPException(
            status_code=400,
            detail="Marks already exist. Use update API."
        )

    new_marks = Marks(
        student_id=data.student_id,
        course_id=data.course_id,
        marks=data.marks
    )

    db.add(new_marks)

    db.commit()

    db.refresh(new_marks)

    return {
        "message": "Marks added successfully",
        "id": new_marks.id,
        "student_id": new_marks.student_id,
        "course_id": new_marks.course_id,
        "marks": new_marks.marks
    }


# =========================
# CREATE MARKS BY ROLL NO
# =========================

@router.post(
    "/roll",
    response_model=MarksResponse
)
def create_marks_by_roll(
    data: MarksCreateByRoll,
    db: Session = Depends(get_db)
):

    student = db.query(Student).filter(
        Student.roll_no == data.roll_no
    ).first()

    if not student:

        raise HTTPException(
            status_code=404,
            detail=f"Student with roll number {data.roll_no} not found"
        )

    course = db.query(Course).filter(
        Course.id == data.course_id
    ).first()

    if not course:

        raise HTTPException(
            status_code=404,
            detail="Course not found"
        )

    if student.course_id != data.course_id:

        raise HTTPException(
            status_code=400,
            detail=f"{student.name} is not enrolled in {course.name}"
        )

    existing_marks = db.query(Marks).filter(
        Marks.student_id == student.id,
        Marks.course_id == data.course_id
    ).first()

    if existing_marks:

        raise HTTPException(
            status_code=400,
            detail=f"Marks already exist for {student.name}. Use update API."
        )

    new_marks = Marks(
        student_id=student.id,
        course_id=data.course_id,
        marks=data.marks
    )

    db.add(new_marks)

    db.commit()

    db.refresh(new_marks)

    return {
        "student_id": student.id,
        "roll_no": student.roll_no,
        "name": student.name,
        "course": course.name,
        "marks": new_marks.marks
    }


# =========================
# GET ALL STUDENT MARKS
# =========================

@router.get(
    "/",
    response_model=list[MarksResponse]
)
def get_all_marks(
    db: Session = Depends(get_db)
):

    records = (
        db.query(Marks)
        .join(Student, Marks.student_id == Student.id)
        .join(Course, Marks.course_id == Course.id)
        .order_by(Course.id, Student.roll_no)
        .all()
    )

    return [
        {
            "student_id": record.student.id,
            "roll_no": record.student.roll_no,
            "name": record.student.name,
            "course": record.course.name,
            "marks": record.marks
        }
        for record in records
    ]


# =========================
# BULK MARKS UPDATE
# =========================

@router.put("/bulk")
def bulk_update_marks(
    data: BulkMarksUpdate,
    db: Session = Depends(get_db)
):

    course = db.query(Course).filter(
        Course.id == data.course_id
    ).first()

    if not course:

        raise HTTPException(
            status_code=404,
            detail="Course not found"
        )

    updated = []

    for item in data.marks:

        student = db.query(Student).filter(
            Student.id == item.student_id
        ).first()

        if not student:

            raise HTTPException(
                status_code=404,
                detail=f"Student {item.student_id} not found"
            )

        if student.course_id != data.course_id:

            raise HTTPException(
                status_code=400,
                detail=f"Student {item.student_id} is not enrolled in this course"
            )

        mark = db.query(Marks).filter(
            Marks.student_id == item.student_id,
            Marks.course_id == data.course_id
        ).first()

        if mark:

            mark.marks = item.marks

        else:

            mark = Marks(
                student_id=item.student_id,
                course_id=data.course_id,
                marks=item.marks
            )

            db.add(mark)

        updated.append(
            {
                "student_id": item.student_id,
                "marks": item.marks
            }
        )

    db.commit()

    return {
        "message": "Bulk marks updated successfully",
        "course_id": data.course_id,
        "updated_students": updated
    }


# =========================
# UPDATE ONE MARK
# =========================

@router.put("/{marks_id}")
def update_marks(
    marks_id: int,
    data: MarksUpdate,
    db: Session = Depends(get_db)
):

    mark = db.query(Marks).filter(
        Marks.id == marks_id
    ).first()

    if not mark:

        raise HTTPException(
            status_code=404,
            detail="Marks record not found"
        )

    mark.marks = data.marks

    db.commit()

    db.refresh(mark)

    return {
        "message": "Marks updated successfully",
        "id": mark.id,
        "student_id": mark.student_id,
        "course_id": mark.course_id,
        "marks": mark.marks
    }