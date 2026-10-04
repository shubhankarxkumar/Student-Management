from pydantic import BaseModel, ConfigDict

class TeacherCreate(BaseModel):

    name: str

    email: str


class TeacherResponse(BaseModel):

    id: int

    name: str

    email: str

    model_config = ConfigDict(from_attributes=True)