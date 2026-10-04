from pydantic import BaseModel, Field, ConfigDict


class MarksCreate(BaseModel):

    student_id: int

    course_id: int

    marks: int = Field(
        ge=0,
        le=100
    )


class MarksUpdate(BaseModel):

    marks: int = Field(
        ge=0,
        le=100
    )


class BulkMarkItem(BaseModel):

    student_id: int

    marks: int = Field(
        ge=0,
        le=100
    )


class BulkMarksUpdate(BaseModel):

    course_id: int

    marks: list[BulkMarkItem]


class MarksCreateByRoll(BaseModel):

    roll_no: int

    course_id: int

    marks: int = Field(
        ge=0,
        le=100
    )


class MarksResponse(BaseModel):

    student_id: int

    roll_no: int

    name: str

    course: str

    marks: int