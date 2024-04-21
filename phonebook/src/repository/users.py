from libgravatar import Gravatar
from sqlalchemy.orm import Session

from src.database.models import User
from src.schemas import UserModel


async def get_user_by_email(email: str, db: Session) -> User:
    """
    The get_user_by_email function returns a user object from the database based on the email address provided.
        Args:
            email (str): The email address of the user to be retrieved.
            db (Session): A connection to a database session.
        Returns:
            User: A single user object matching the provided email address.
    
    :param email: str: Specify the type of data that is being passed in
    :param db: Session: Pass the database session to the function
    :return: A single user object that matches the email address provided
    :doc-author: Trelent
    """
    return db.query(User).filter(User.email == email).first()


async def create_user(body: UserModel, db: Session) -> User:
    """
    The create_user function creates a new user in the database.
        Args:
            body (UserModel): The UserModel object containing the data to be inserted into the database.
            db (Session): The SQLAlchemy Session object used to interact with the database.
        Returns:
            User: A newly created user from the provided data.
    
    :param body: UserModel: Pass in the user object that is created when a new user registers
    :param db: Session: Create a new user in the database
    :return: A user object
    :doc-author: Trelent
    """
    avatar = None
    try:
        g = Gravatar(body.email)
        avatar = g.get_image()
    except Exception as e:
        print(e)
    # new_user = User(**body.dict(), avatar=avatar)
    new_user = User(**body.dict(), avatar=avatar)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user


async def update_token(user: User, token: str | None, db: Session) -> None:
    """
    The update_token function updates the refresh_token field of a user in the database.
    
    :param user: User: Get the user's id
    :param token: str | None: Set the refresh_token field in the user table
    :param db: Session: Commit the changes to the database
    :return: None
    :doc-author: Trelent
    """
    user.refresh_token = token
    db.commit()

async def confirmed_email(email: str, db: Session) -> None:
    """
    The confirmed_email function sets the confirmed field of a user to True.
    
    :param email: str: Get the email of the user who is trying to confirm their account
    :param db: Session: Access the database
    :return: None
    :doc-author: Trelent
    """
    user = await get_user_by_email(email, db)
    user.confirmed = True
    db.commit()
    
async def update_avatar(email, url: str | None, db: Session) -> User:
    """
    The update_avatar function updates the avatar of a user.
    
    Args:
        email (str): The email address of the user to update.
        url (str | None): The URL to set as the new avatar for this user, or None if no change is desired.
        db (Session): A database session object used for querying and updating data in our database.  This is passed in by FastAPI so we don't have to create it ourselves!  See https://fastapi.tiangolo.com/advanced/dependencies/#database-access-with-sqlalchemycore for
    
    :param email: Find the user in the database
    :param url: str | None: Specify the type of the url parameter
    :param db: Session: Pass the database session to the function
    :return: A user object
    :doc-author: Trelent
    """
    user = await get_user_by_email(email, db)
    user.avatar = url
    db.commit()
    return user


