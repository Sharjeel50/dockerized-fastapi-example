import threading
from typing import List, Optional

from sqlalchemy.orm import Session
from ...settings.config import settings
from ...api_v1.deps import get_db
from ...crud import base as crd_inst
from ...models.models import Instructor as InstMdl
from fastapi import Depends, HTTPException, status, APIRouter, UploadFile, File
from ...schemas.instructor import InstructorCreate, InstructorUpdate, Instructor

instructors = APIRouter()
crd = crd_inst.BaseCrud(InstMdl, Instructor)

@instructors.post("/")
def create(usc: InstructorCreate = Depends(InstructorCreate.as_form), db: Session = Depends(get_db), adi_license: UploadFile = File(...)):
    res = threading.Thread(target=upload_image, args=(s3, settings.S3_BUCKET_ADI, adi_license.file, adi_license.filename,)).start()
    db_user = crd.get_user_by_email(db, email=usc.email)
    if db_user:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Email already registered")
    return crd.create_user(db=db, usc=usc, image_url=adi_license.filename)


@instructors.get("/", response_model=List[Instructor])
def read_all(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    db_users = crd.get_users(db, skip=skip, limit=limit)
    return db_users


@instructors.get("/{user_id}", response_model=Instructor)
def read(user_id: str, db: Session = Depends(get_db)):
    db_user = crd.get_user(db, user_id=user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user


@instructors.delete("/{user_id}")
def delete(user_id: str, db: Session = Depends(get_db)):
    del_user = crd.delete_user(db, user_id)
    if del_user:
        return status.HTTP_200_OK
    raise HTTPException(status_code=400, detail="User not found")


@instructors.patch("/{user_id}")
def update(user_id: str, user: InstructorUpdate = Depends(InstructorUpdate.as_form), db: Session = Depends(get_db),
           profile_images: Optional[List[UploadFile]] = File(None), adi_license: Optional[UploadFile] = File(None)):

    current_user = crd.get_user(db, user_id)

    image_keys = []
    # Exception wont be raised here.
    for img in profile_images:
        a = threading.Thread(target=upload_image, args=(s3, settings.S3_BUCKET_ADI, img.file, img.filename,)).start()
        image_keys.append(img.filename)

    if adi_license:
        threading.Thread(target=upload_image, args=(s3, settings.S3_BUCKET_ADI, adi_license.file, adi_license.filename,)).start()

    if current_user:
        updated_user = crd.update_user(db, current_user, user, image_keys=image_keys, adi_license=adi_license.filename)
        return updated_user
    else:
        raise HTTPException(status_code=400, detail="User not found")
