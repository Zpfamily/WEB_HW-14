from fastapi import APIRouter, Depends, status, UploadFile, File
from sqlalchemy.orm import Session
import cloudinary
import cloudinary.uploader

from src.database.db import get_db
from src.database.models import User
from src.repository import users as repository_users
from src.services.auth import auth_service
from src.conf.config import settings
from src.schemas import UserDb, UserResponse

router = APIRouter(prefix="/users", tags=["users"])


@router.get("/me/", response_model=UserDb)
async def read_users_me(current_user: User = Depends(auth_service.get_current_user)):
    """
    The read_users_me function returns the current user's information.
        ---
        get:
          tags: [users] # This is a tag that can be used to group operations by resources or any other qualifier.
          summary: Returns the current user's information.
          description: Returns the current user's information based on their JWT token in their request header.
          responses: # The possible responses this operation can return, along with descriptions and examples of each response type (if applicable).
            &quot;200&quot;:  # HTTP status code 200 indicates success! In this case, it means we successfully returned a User
    
    :param current_user: User: Get the current user from the database
    :return: The current_user object
    :doc-author: Trelent
    """
    return current_user


@router.patch('/avatar', response_model=UserDb)
async def update_avatar_user(file: UploadFile = File(), current_user: User = Depends(auth_service.get_current_user),
                             db: Session = Depends(get_db)):
    """
    The update_avatar_user function updates the avatar of a user.
        Args:
            file (UploadFile): The file to be uploaded.
            current_user (User): The currently logged in user.
            db (Session): A database session object for interacting with the database.
    
    :param file: UploadFile: Get the file from the request body
    :param current_user: User: Get the current user from the database
    :param db: Session: Connect to the database
    :return: A user
    :doc-author: Trelent
    """
    cloudinary.config(
        # cloud_name=settings.cloudinary_name,
        # api_key=settings.cloudinary_api_key,
        # api_secret=settings.cloudinary_api_secret,
        CLOUDINARY_URL = settings.CLOUDINARY_URL,
        secure=True
    )

    r = cloudinary.uploader.upload(file.file, public_id=f'contacts/{current_user.username}', overwrite=True)
    src_url = cloudinary.CloudinaryImage(f'contacts/{current_user.username}')\
                        .build_url(width=250, height=250, crop='fill', version=r.get('version'))
    user = await repository_users.update_avatar(current_user.email, src_url, db)
    return user



