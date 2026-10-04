from fastapi import FastAPI

from database import engine, Base

# Import models so SQLAlchemy knows about all tables
from models.student import Student
from models.teacher import Teacher
from models.course import Course
from models.marks import Marks

from routers import (
    student,
    teacher,
    course,
    marks,
    info
)


Base.metadata.create_all(
    bind=engine
)


app = FastAPI(
    title="Student Management System",
    description="Student, Teacher, Course and Marks Management API",
    version="1.0.0"
)


app.include_router(
    student.router
)

app.include_router(
    teacher.router
)

app.include_router(
    course.router
)

app.include_router(
    marks.router
)

app.include_router(
    info.router
)


@app.get("/")
def home():

    return {
        "message": "Student Management API is running"
    }