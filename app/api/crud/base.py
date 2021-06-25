import uuid
from typing import Any, Optional, List, TypeVar

from fastapi import UploadFile
from sqlalchemy.orm import Session
from fastapi.encoders import jsonable_encoder
from ..security.security import get_password_hash
from ..db.database import Base


ModelType = TypeVar("ModelType", bound=Base)

class BaseCrud:
    def __init__(self, model, usr: Optional[Any] = None, usp: Optional[Any] = None):
        self.__model = model
        self.__usr = usr
        self.__usp = usp

    def get_user(self, db: Session, user_id: str):
        return db.query(self.__model).filter(self.__model.id == user_id).first()

    def get_user_by_email(self, db: Session, email: str):
        return db.query(self.__model).filter(self.__model.email == email).first()

    def get_users(self, db: Session, skip: int = 0, limit: int = 100):
        return db.query(self.__model).offset(skip).limit(limit).all()

    def create_user(self, db: Session, usc: Any, image_url: Optional[str] = None):
        _id = str(uuid.uuid4())
        _hsed_pw = get_password_hash(usc.hashed_password)
        db_user = self.__model(id=_id, **usc.dict())
        db_user.hashed_password = _hsed_pw
        if image_url:
            db_user.adi_license = image_url
        db.add(db_user)
        db.commit()
        db.refresh(db_user)
        return db_user

    def delete_user(self, db: Session, _id: str):
        user = db.query(self.__model).filter(self.__model.id == _id).first()
        print(f"User: {user}")
        if user:
            db.delete(user)
            db.commit()
            return True
        return False

    def update_user(self, db: Session, db_obj: ModelType, usup: Any, image_keys: Optional[List[str]] = None,
                    adi_license: Optional[str] = None):

        obj_data = jsonable_encoder(db_obj)
        if isinstance(usup, dict):
            update_data = usup
        else:
            update_data = usup.dict(exclude_unset=True)

        if "hashed_password" in update_data:
            hashed_password = get_password_hash(update_data["hashed_password"])
            del update_data["hashed_password"]
            update_data["hashed_password"] = hashed_password

        if adi_license:
            update_data["adi_license"] = adi_license

        for field in obj_data:
            if field in update_data:
                if update_data[field] is not None:
                    setattr(db_obj, field, update_data[field])

        # fields = ['profile_image_one', 'profile_image_two', 'profile_image_three']
        # for i in range(len(image_keys)):
        #     if image_keys[i] != '' or image_keys[i] is not None:
        #         setattr(db_obj, fields[i], image_keys[i])
        #     else:
        #         setattr(db_obj, fields[i], '')

        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

