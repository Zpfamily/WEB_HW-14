from os import environ
from pathlib import Path
import os

from dotenv import load_dotenv
from pydantic_settings import BaseSettings
import cloudinary

BASE_PATH = Path(__file__).resolve().parent.parent.parent.parent
# load_dotenv(BASE_PATH.joinpath(".env"))
load_dotenv(BASE_PATH / ".env")
APP_ENV = environ.get("APP_ENV")


class Settings(BaseSettings):
    app_mode: str = "prod"
    app_name: str = "contacts"
    app_host: str = "0.0.0.0"
    app_port: int = 8000
    sqlalchemy_database_url: str | None = None
    token_secret_key: str = "some_SuPeR_key"
    token_algorithm: str = "HS256"
    mail_username: str = environ.get("MAIL_USERNAME")
    mail_password: str = environ.get("MAIL_PASSWORD")
    mail_from: str = "user@example.com"
    mail_port: int = 465
    mail_server: str = ""
    mail_from_name: str = ""
    redis_host: str = "localhost"
    redis_port: int = 6379
    # cloudinary_name: str
    # cloudinary_api_key: int
    # cloudinary_api_secret: str
    CLOUDINARY_URL : str = environ.get("CLOUDINARY_URL")
 


    class Config:
        extra = "ignore"
        # TESTED FIRST USED ENV variables, even if file defined.
        # env_file = BASE_PATH.joinpath(f".env-{APP_ENV}") if APP_ENV else BASE_PATH.joinpath(".env")
        env_file = ".env"
        env_file_encoding = "utf-8"


settings = Settings()

# if __name__ == "__main__":
#     print(settings.Config.env_file)
#     print(settings)