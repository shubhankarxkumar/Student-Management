"""
Seed script.

Wipes the existing data and loads the starting data:
3 teachers, 3 courses, 10 students per course.
Every student gets a random mark between 70 and 100.

Run from the project folder:
    python seed.py
"""

import random

from database import Base, SessionLocal, engine

from models.teacher import Teacher
from models.course import Course
from models.student import Student
from models.marks import Marks


TEACHERS = [
    {"name": "Andrew", "email": "andrew@school.com"},
    {"name": "Mathew", "email": "mathew@school.com"},
    {"name": "Ilyas", "email": "iliyas@school.com"},
]


COURSES = [
    {"name": "Python", "teacher": "Andrew"},
    {"name": "FastAPI", "teacher": "Mathew"},
    {"name": "AI-ML", "teacher": "Ilyas"},
]


STUDENTS = {
    "Python": [
        "Hana Gardner",
        "Alan Ball",
        "Abby Hutchinson",
        "Korbin McFarland",
        "Annika West",
        "Diego Owen",
        "Mikayla Buchanan",
        "Enrique White",
        "Layla Yoder",
        "Johan Byrd",
    ],

    "FastAPI": [
        "Cecilia Gross",
        "Quinn Gentry",
        "Amelie Cunningham",
        "Alejandro Buckley",
        "Theodora Hammond",
        "Francis Salgado",
        "Avalynn Chandler",
        "Royal Pearson",
        "Kiara Ferguson",
        "Miguel McCullough",
    ],

    "AI-ML": [
        "Jessica May",
        "Finley Moss",
        "Bianca Li",
        "Jorge Pennington",
        "Yareli Lu",
        "Duncan Navarro",
        "Winter Parrish",
        "Karsyn Peck",
        "Crystal Briggs",
        "Case Sheppard",
    ],
}


# Roll numbers start at 1 and keep counting across all courses.
ROLL_NO_START = 1

# Every student gets a random mark between these two values.
MIN_MARKS = 70
MAX_MARKS = 100


def wipe(db):

    db.query(Marks).delete()
    db.query(Student).delete()
    db.query(Course).delete()
    db.query(Teacher).delete()

    db.commit()


def seed():

    Base.metadata.create_all(bind=engine)

    db = SessionLocal()

    try:

        wipe(db)

        teachers = {}

        for item in TEACHERS:

            teacher = Teacher(
                name=item["name"],
                email=item["email"]
            )

            db.add(teacher)
            db.flush()

            teachers[teacher.name] = teacher

        roll_no = ROLL_NO_START

        for course_item in COURSES:

            course = Course(
                name=course_item["name"],
                teacher_id=teachers[course_item["teacher"]].id
            )

            db.add(course)
            db.flush()

            for name in STUDENTS[course_item["name"]]:

                student = Student(
                    roll_no=roll_no,
                    name=name,
                    course_id=course.id
                )

                db.add(student)
                db.flush()

                db.add(
                    Marks(
                        student_id=student.id,
                        course_id=course.id,
                        marks=random.randint(MIN_MARKS, MAX_MARKS)
                    )
                )

                roll_no = roll_no + 1

        db.commit()

        total_students = sum(len(v) for v in STUDENTS.values())

        print("Seed complete")
        print(f"  teachers : {len(TEACHERS)}")
        print(f"  courses  : {len(COURSES)}")
        print(f"  students : {total_students}")
        print(f"  marks    : {total_students} (random {MIN_MARKS}-{MAX_MARKS})")

    finally:

        db.close()


if __name__ == "__main__":

    seed()
