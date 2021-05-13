import inspect
import boto3
from botocore.exceptions import ClientError
from starlette import status

from ..models import models
from ..settings.config import settings
from fastapi import Form, HTTPException
from typing import Generator, Type
from pydantic.main import BaseModel
from ..db.database import SessionLocal, engine

models.Base.metadata.create_all(bind=engine)


def get_db() -> Generator:
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def as_form(cls: Type[BaseModel]):
    """
    Adds an as_form class method to decorated models. The as_form class method
    can be used with FastAPI endpoints
    """
    new_params = [
        inspect.Parameter(
            field.alias,
            inspect.Parameter.POSITIONAL_ONLY,
            default=(Form(field.default) if not field.required else Form(...)),
        )
        for field in cls.__fields__.values()
    ]

    async def _as_form(**data):
        return cls(**data)

    sig = inspect.signature(_as_form)
    sig = sig.replace(parameters=new_params)
    _as_form.__signature__ = sig
    setattr(cls, "as_form", _as_form)
    return cls


def upload_image(client, bucket, file, key):
    s = client.put_object(Body=file, Bucket=bucket, Key=key, ContentType='image/png')
    status_code = s['ResponseMetadata']['HTTPStatusCode']
    if status_code != 200:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Image failed to upload.")
    return True


def check_key(client, bucket, key):
    try:
        client.head_object(Bucket=bucket, Key=key)
    except ClientError as e:
        return int(e.response['Error']['Code']) != 404
    return True


s3 = boto3.client('s3', aws_access_key_id=settings.AWS_SECRET_KEY_ID,
                  aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY)
