from ..db.database import Base
from sqlalchemy.orm import relationship
from sqlalchemy import Column, String, Boolean, Date

class UserBase(Base):
    __abstract__ = True
    id = Column(String, primary_key=True)
    full_name = Column(String, nullable=True)
    phone_number = Column(String, nullable=True)
    email = Column(String, unique=True, index=True, nullable=True)
    hashed_password = Column(String, nullable=False)
    is_active = Column(Boolean, default=True, nullable=True)
    is_superuser = Column(Boolean, default=False, nullable=True)
    sex = Column(String, nullable=True)
    car_type = Column(String, nullable=True)
    profile_image_one = Column(String, nullable=True)
    # Lessons = relationship("Lesson", back_populates="owner")

class Instructor(UserBase):
    __tablename__ = "instructors"
    area_covered = Column(String, index=True)
    driving_school_name = Column(String)
    driving_school_description = Column(String, nullable=True)
    adi_license = Column(String)
    profile_image_two = Column(String, nullable=True)
    profile_image_three = Column(String, nullable=True)

    def __repr__(self):
        return f"{self.id} - {self.full_name} - {self.phone_number} - {self.email} - {self.hashed_password} - " \
               f"{self.sex} - {self.car_type} - {self.area_covered} - {self.driving_school_name} "

class Learner(UserBase):
    __tablename__ = "learners"
    date_of_birth = Column(Date, index=True)
    address = Column(String, index=True)


