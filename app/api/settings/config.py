import os
from typing import Optional
from pydantic import BaseSettings, EmailStr

# Mac users use this to set environment variables :)
# touch ~/.bash_profile; open ~/.bash_profile

class Settings(BaseSettings):

    POSTGRES_SERVER: str = os.getenv['POSTGRES_SERVER']
    POSTGRES_USER: str = os.environ['POSTGRES_USER']
    POSTGRES_PASSWORD: str = os.environ['POSTGRES_PASSWORD']
    POSTGRES_DB: str = os.environ['POSTGRES_DB']
    S3_BUCKET_ADI: str = 'test'
    S3_BUCKET_L: str = 'test'

    # POSTGRES_SERVER: str = "localhost:5431"
    # POSTGRES_USER: str = "sj1234"
    # POSTGRES_PASSWORD: str = "123"
    # POSTGRES_DB: str = "sj1234"

    # EMAIL_RESET_TOKEN_EXPIRE_HOURS: int = 48

    # SMTP_TLS: bool = True
    # SMTP_PORT: Optional[int] = None
    # SMTP_HOST: Optional[str] = None
    # SMTP_USER: Optional[str] = None
    # SMTP_PASSWORD: Optional[str] = None
    # EMAILS_FROM_EMAIL: Optional[EmailStr] = None
    # EMAILS_FROM_NAME: Optional[str] = None

    AWS_SECRET_KEY_ID: str = os.environ['AWS_SECRET_KEY_ID']
    AWS_SECRET_ACCESS_KEY: str = os.environ['AWS_SECRET_ACCESS_KEY']

    # EMAIL_TEMPLATES_DIR: str = ""

    # EMAIL_TEST_USER: EmailStr = "testeremail@gmail.com"
    # FIRST_SUPERUSER: EmailStr
    # FIRST_SUPERUSER_PASSWORD: Optional[str] = None
    # USERS_OPEN_REGISTRATION: bool = False

    class Config:
        case_sensitive = True


settings = Settings()
