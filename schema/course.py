from pydantic import BaseModel, ConfigDict


class CourseCreate(BaseModel):

    name: str

    teacher_id: int


class CourseResponse(BaseModel):

    id: int

    name: str

    teacher_id: int

    model_config = ConfigDict(from_attributes=True)