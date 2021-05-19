import threading
from typing import List, Optional
from sqlalchemy.orm import Session

# from ..deps import upload_image, s3
from ...api_v1 import deps as d
from ...crud import base as crd_inst
from ...models.models import Learner as InstMdl
from fastapi import Depends, HTTPException, status, APIRouter, UploadFile, File
from ...schemas.leaners import LearnerUpdate, LearnerCreate, Learner
from ...settings.config import settings

learners = APIRouter()
crd = crd_inst.BaseCrud(InstMdl)


@learners.post("/")
def create(user: LearnerCreate, db: Session = Depends(d.get_db)):
    db_user = crd.get_user_by_email(db, email=user.email)
    if db_user:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Email already registered")
    return crd.create_user(db=db, usc=user)

@learners.get("/", response_model=List[Learner])
def read_all(skip: int = 0, limit: int = 100, db: Session = Depends(d.get_db)):
    db_users = crd.get_users(db, skip=skip, limit=limit)
    return db_users

@learners.get("/{user_id}", response_model=Learner)
def read(user_id: str, db: Session = Depends(d.get_db)):
    db_user = crd.get_user(db, user_id=user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user

@learners.delete("/{user_id}")
def delete(user_id: str, db: Session = Depends(d.get_db)):
    del_user = crd.delete_user(db, user_id)
    if del_user:
        return status.HTTP_200_OK
    raise HTTPException(status_code=400, detail="User not found")

@learners.patch("/{user_id}")
def update(user_id: str, user: LearnerUpdate = Depends(LearnerUpdate.as_form), db: Session = Depends(d.get_db),
           profile_images: Optional[List[UploadFile]] = File(None)):
    current_user = crd.get_user(db, user_id)
    # threading.Thread(target=upload_image, args=(s3, settings.S3_BUCKET_L, profile_images[0].file, profile_images[0].filename,)).start()
    if current_user:
        # updated_user = crd.update_user(db, current_user, user, image_keys=[profile_images[0].filename])
        updated_user = crd.update_user(db, current_user, user)
        return updated_user
    else:
        raise HTTPException(status_code=400, detail="User not found")



