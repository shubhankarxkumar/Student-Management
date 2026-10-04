from pydantic import BaseModel, ConfigDict



class StudentCreate(BaseModel):

    roll_no: int

    name: str

    course_id: int


class StudentResponse(BaseModel):

    id: int

    roll_no: int

    name: str

    course_id: int

    model_config = ConfigDict(from_attributes=True)


class StudentCourseUpdate(BaseModel):

    course_id: int

