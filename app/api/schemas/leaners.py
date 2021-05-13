from typing import List, Optional
from pydantic import BaseModel
from datetime import date
from ..api_v1.deps import as_form

class LearnerCreate(BaseModel):
    sex: str
    car_type: str
    full_name: str
    email: str
    phone_number: str
    date_of_birth: date
    hashed_password: str
    address: str

class InstructorDelete(BaseModel):
    id: str

@as_form
class LearnerUpdate(BaseModel):
    car_type: Optional[str] = None
    full_name: Optional[str] = None
    email: Optional[str] = None
    hashed_password: Optional[str] = None
    phone_number: Optional[str] = None
    address: Optional[str] = None
    date_of_birth: Optional[date] = None

class Learner(BaseModel):
    id: str
    is_active: bool
    is_superuser: bool
    car_type: str
    full_name: str
    email: str
    phone_number: str
    date_of_birth: date
    address: str
    profile_image_one: Optional[str] = None

    class Config:
        orm_mode = True



