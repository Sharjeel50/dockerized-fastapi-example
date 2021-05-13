from typing import List, Optional

from pydantic import BaseModel
from ..api_v1.deps import as_form

@as_form
class InstructorCreate(BaseModel):
    sex: str
    car_type: str
    area_covered: str
    full_name: str
    email: str
    phone_number: str
    driving_school_name: str
    driving_school_description: Optional[str] = None
    hashed_password: str


class InstructorDelete(BaseModel):
    id: str

@as_form
class InstructorUpdate(BaseModel):
    car_type: Optional[str] = None
    full_name: Optional[str] = None
    email: Optional[str] = None
    hashed_password: Optional[str] = None
    phone_number: Optional[str] = None
    area_covered: Optional[str] = None
    driving_school_name: Optional[str] = None
    driving_school_description: Optional[str] = None

class Instructor(BaseModel):
    id: str
    full_name: str
    phone_number: str
    email: str
    is_active: bool
    is_superuser: bool
    sex: str
    car_type: str
    area_covered: str
    driving_school_name: str
    driving_school_description: Optional[str] = None
    adi_license: str
    profile_image_one: Optional[str] = None
    profile_image_two: Optional[str] = None
    profile_image_three: Optional[str] = None

    class Config:
        orm_mode = True



