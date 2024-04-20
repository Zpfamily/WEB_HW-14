from datetime import date, timedelta

from sqlalchemy.orm import Session

from src.schemas import ContactModel,ContactFavoriteModel
from src.database.models import Contact, User



async def get_contacts(db: Session, user_id: int,  skip: int, limit: int, favorite: bool|None = None):
    """
    The get_contacts function returns a list of contacts for the user.
        
    
    :param db: Session: Pass the database session to the function
    :param user_id: int: Filter the contacts by user_id
    :param skip: int: Skip the first n contacts
    :param limit: int: Limit the number of contacts returned
    :param favorite: bool|None: Filter the contacts by favorite
    :return: A list of contacts
    :doc-author: Trelent
    """
    query = db.query(Contact).filter_by(user_id=user_id)
    if favorite is not None:
        query = query.filter_by(user_id=user_id)
    contacts = query.offset(skip).limit(limit).all()
    return contacts


async def get_contact_by_id(contact_id: int, user_id: int, db: Session):
    """
    The get_contact_by_id function returns a contact object from the database based on the id of that contact.
        Args:
            contact_id (int): The id of the desired Contact object.
            user_id (int): The id of the User who owns this Contact.
            db (Session): A connection to our database, used for querying and updating data in our tables.
    
    :param contact_id: int: Filter the database query by id
    :param user_id: int: Filter the contacts by user_id
    :param db: Session: Pass the database session to the function
    :return: A contact object
    :doc-author: Trelent
    """
    contact = db.query(Contact).filter_by(id=contact_id, user_id=user_id).first()
    return contact


async def get_contact_by_email(email: str, user_id: int, db: Session):
    """
    The get_contact_by_email function returns a contact object from the database based on the email address and user_id.
        Args:
            email (str): The email address of the contact to be retrieved.
            user_id (int): The id of the user who owns this contact.
            db (Session, optional): SQLAlchemy Session instance. Defaults to None.
    
    :param email: str: Filter the query by email
    :param user_id: int: Filter the results of the query by user_id
    :param db: Session: Pass in the database session
    :return: The first contact that matches the email and user_id
    :doc-author: Trelent
    """
    contact = db.query(Contact).filter_by(email=email, user_id=user_id).first()
    return contact


async def create(body: ContactModel, user_id: int, db: Session):
    """
    The create function creates a new contact in the database.
        
    
    :param body: ContactModel: Get the data from the request body
    :param user_id: int: Get the user_id from the database
    :param db: Session: Access the database
    :return: A contact object
    :doc-author: Trelent
    """
    contact = Contact(**body.model_dump())
    contact.user_id = user_id
    db.add(contact)
    db.commit()
    db.refresh(contact)
    return contact


async def update(contact_id: int, body: ContactModel, user_id: int, db: Session):
    """
    The update function updates a contact in the database.
        Args:
            contact_id (int): The id of the contact to update.
            body (ContactModel): The updated information for the specified contact.
            user_id (int): The id of the user who owns this specific contact.
    
    :param contact_id: int: Identify the contact to be updated
    :param body: ContactModel: Get the data from the request body
    :param user_id: int: Make sure that the user is only able to update their own contacts
    :param db: Session: Create a connection to the database
    :return: A contact object
    :doc-author: Trelent
    """
    contact = await get_contact_by_id(contact_id, user_id, db)
    if contact:
        contact.first_name = body.first_name
        contact.last_name = body.last_name
        contact.email = body.email
        contact.phone = body.phone
        contact.birthday = body.birthday
        contact.comments = body.comments
        contact.favorite = body.favorite
        db.commit()
    return contact


async def favorite_update(contact_id: int, body: ContactFavoriteModel, user_id: int, db: Session):
    """
    The favorite_update function updates the favorite field of a contact.
        Args:
            contact_id (int): The id of the contact to update.
            body (ContactFavoriteModel): A ContactFavoriteModel object containing the new value for favorite.
            user_id (int): The id of the user who owns this contact.
        Returns: 
            Contact: An updated version of this Contact.
    
    :param contact_id: int: Get the contact by id
    :param body: ContactFavoriteModel: Get the favorite value from the request body
    :param user_id: int: Make sure that the user is only updating their own contact information
    :param db: Session: Pass the database session to the function
    :return: A contactmodel object
    :doc-author: Trelent
    """
    contact = await get_contact_by_id(contact_id, user_id, db)
    if contact:
        contact.favorite = body.favorite
        db.commit()
    return contact


async def delete(contact_id: int, user_id: int, db: Session):
    """
    The delete function deletes a contact from the database.
        
    
    :param contact_id: int: Specify the contact to delete
    :param user_id: int: Ensure that the user is only deleting their own contacts
    :param db: Session: Pass the database session to the function
    :return: A contact object, which is what we want to test
    :doc-author: Trelent
    """
    contact = await get_contact_by_id(contact_id, user_id, db)
    if contact:
        db.delete(contact)
        db.commit()
    return contact


async def search_contacts(param: dict, user_id: int, db: Session):
    """
    The search_contacts function searches for contacts in the database.
        Args:
            param (dict): A dictionary containing search parameters.  The keys are &quot;first_name&quot;, &quot;last_name&quot;, and &quot;email&quot;.  The values are strings to be searched for in the corresponding fields of a contact record.
            user_id (int): An integer representing the id of a user who owns contacts being searched for.  
            db (Session): A SQLAlchemy Session object used to query the database with an ORM model class called Contact, which is defined below this function definition as a subclass of Base, which is also defined
    
    :param param: dict: Pass in a dictionary of parameters that will be used to filter the contacts
    :param user_id: int: Filter the contacts by user_id
    :param db: Session: Pass the database session to the function
    :return: A query object, not a list of contacts
    :doc-author: Trelent
    """
    query = db.query(Contact).filter_by(user_id=user_id)
    first_name = param.get("first_name")
    last_name = param.get("last_name")
    email = param.get("email")
    if first_name:
        query = query.filter(Contact.first_name.ilike(f"%{first_name}%"))
    if last_name:
        query = query.filter(Contact.last_name.ilike(f"%{last_name}%"))   
    if email:
        query = query.filter(Contact.email.ilike(f"%{email}%"))   
    contacts = query.offset(param.get("skip")).limit(param.get("limit"))
    return contacts


async def search_birthday(param: dict, user_id: int, db: Session):
    """
    The search_birthday function searches for contacts with birthdays in the next 7 days.
        Args:
            param (dict): The parameters to filter by.
            user_id (int): The id of the user who is making this request.
            db (Session, optional): SQLAlchemy Session instance. Defaults to None.&lt;/code&gt;
    
    :param param: dict: Pass in the query parameters from the url
    :param user_id: int: Filter the contacts by user_id
    :param db: Session: Pass the database connection to the function
    :return: A query object, not a list of contacts
    :doc-author: Trelent
    """
    days:int = int(param.get("days", 7)) + 1
    filter_afetr = date.today()
    filter_before = date.today() + timedelta(days = days)
    query = db.query(Contact).filter_by(user_id=user_id)
    query = query.filter(Contact.birthday > filter_afetr, Contact.birthday <= filter_before)
    contacts = query.offset(param.get("skip")).limit(param.get("limit"))
    return contacts