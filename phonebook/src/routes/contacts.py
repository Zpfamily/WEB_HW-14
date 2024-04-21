from typing import List

from fastapi import Path, Depends, HTTPException, Query, status, APIRouter
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from src.database.db import get_db
from src.schemas import ContactFavoriteModel, ContactModel, ContactResponse
from src.repository import contacts as repository_contacts
from src.services.auth import auth_service
from src.database.models import User
from fastapi_limiter.depends import RateLimiter


router = APIRouter(prefix="/contacts", tags=["contacts"])


@router.get("/search", response_model=List[ContactResponse])
async def search_contacts(
    first_name: str = None,
    last_name: str = None,
    email: str = None,
    skip: int = 0,
    limit: int = Query(default=10, le=100, ge=10),
    db: Session = Depends(get_db),
    current_user: User = Depends(auth_service.get_current_user),
):
    """
    The search_contacts function searches for contacts in the database.
        Args:
            first_name (str): The first name of the contact to search for.
            last_name (str): The last name of the contact to search for.
            email (str): The email address of the contact to search for.
    
    :param first_name: str: Search for a contact by first name
    :param last_name: str: Search for a contact by last name
    :param email: str: Search for contacts by email
    :param skip: int: Skip the first n records in the database
    :param limit: int: Limit the number of contacts returned
    :param le: Limit the number of results returned
    :param ge: Set the minimum value of the limit parameter
    :param db: Session: Get the database session
    :param current_user: User: Get the current user from the database
    :param : Filter the contacts by first name, last name or email
    :return: A list of contacts
    :doc-author: Trelent
    """
    contacts = None
    if first_name or last_name or email:
        param = {
            "first_name": first_name,
            "last_name": last_name,
            "email": email,
            "skip": skip,
            "limit": limit,
        }
        user_id = current_user.id
        contacts = await repository_contacts.search_contacts(param, db, user_id,)
    if contacts is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Not found")
    return contacts

@router.get("/search/birtdays", response_model=List[ContactResponse])
async def search_contacts(
    days: int = Query(default=7, le=30, ge=1),
    skip: int = 0,
    limit: int = Query(default=10, le=100, ge=10),
    db: Session = Depends(get_db),
    current_user: User = Depends(auth_service.get_current_user),
):
    """
    The search_contacts function searches for contacts that have birthdays within the next 7 days.
        The search_contacts function is a GET request to /api/v0/contacts/search?days=7&amp;skip=0&amp;limit=10
        The search_contacts function returns a list of contacts with birthdays in the next 7 days.
    
    
    :param days: int: Set the number of days to search for birthdays
    :param le: Set the maximum value for a parameter
    :param ge: Set a minimum value for the parameter
    :param skip: int: Skip the first n records
    :param limit: int: Limit the number of results returned
    :param le: Set a maximum value for the parameter
    :param ge: Set the minimum value of the parameter
    :param db: Session: Get the database session
    :param current_user: User: Get the user id of the current user
    :param : Get the current user from the database
    :return: A list of contacts
    :doc-author: Trelent
    """
    contacts = None
    if days:
        param = {
            "days": days,
            "skip": skip,
            "limit": limit,
        }
        contacts = await repository_contacts.search_birthday(param, current_user.id, db)
    if contacts is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Not found")
    return contacts

@router.get("", response_model=List[ContactResponse])
async def get_contacts(
    skip: int = 0,
    limit: int = Query(default=10, le=100, ge=10),
    favorite: bool = None, 
    db: Session = Depends(get_db),
    current_user: User = Depends(auth_service.get_current_user),
):
    """
    The get_contacts function returns a list of contacts.
        The function takes in the following parameters:
            skip (int): The number of contacts to skip before returning results.
            limit (int): The maximum number of contacts to return per page.
            favorite (bool): A boolean value indicating whether or not the contact is a favorite contact for the user making this request.  If True, only return favorite contacts; if False, only return non-favorite contacts; if None, do not filter by favorites status.
    
    :param skip: int: Skip a number of records in the database
    :param limit: int: Limit the number of contacts returned
    :param le: Limit the maximum number of results that can be returned
    :param ge: Specify the minimum value of a number
    :param favorite: bool: Filter the contacts by favorite
    :param db: Session: Pass the database session to the repository layer
    :param current_user: User: Get the user id from the token
    :param : Skip the first n contacts
    :return: A list of contacts
    :doc-author: Trelent
    """
    contacts = await repository_contacts.get_contacts(db=db, skip=skip, user_id=current_user.id, limit=limit, favorite=favorite)
    return contacts


@router.get("/{contact_id}", response_model=ContactResponse)
async def get_contact(contact_id: int = Path(ge=1), db: Session = Depends(get_db),current_user: User = Depends(auth_service.get_current_user),):
    """
    The get_contact function returns a contact by id.
        Args:
            contact_id (int): The id of the contact to be returned.
            db (Session, optional): SQLAlchemy Session. Defaults to Depends(get_db).
            current_user (User, optional): User object from auth middleware. Defaults to Depends(auth_service.get_current_user).
    
    :param contact_id: int: Get the contact_id from the url
    :param db: Session: Pass a database session to the function
    :param current_user: User: Get the current user from the database
    :param : Get the contact id from the url
    :return: A contact object
    :doc-author: Trelent
    """
    contact = await repository_contacts.get_contact_by_id(contact_id, current_user.id, db)
    if contact is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Not found")
    return contact


@router.post("", response_model=ContactResponse, status_code=status.HTTP_201_CREATED,
description='No more than 10 requests per minute', dependencies=[Depends(RateLimiter(times=10, seconds=60))])
async def create_contact(body: ContactModel, db: Session = Depends(get_db),current_user: User = Depends(auth_service.get_current_user),):
    """
    The create_contact function creates a new contact in the database.
        Args:
            body (ContactModel): The contact to create.
            db (Session, optional): SQLAlchemy Session. Defaults to Depends(get_db).
    
    :param body: ContactModel: Pass the contact model to the function
    :param db: Session: Pass the database session to the repository
    :param current_user: User: Get the user id from the token
    :param : Get the contact by id
    :return: A contactmodel
    :doc-author: Trelent
    """
    contact = await repository_contacts.get_contact_by_email(body.email, current_user.id, db)
    if contact:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT, detail=f"Email is exist!"
        )
    try:
        contact = await repository_contacts.create(body, current_user.id, db)
    except IntegrityError as err:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=f"Error: {err}"
        )
    return contact


@router.put("/{contact_id}", response_model=ContactResponse)
async def update_contact(
    body: ContactModel, contact_id: int = Path(ge=1), db: Session = Depends(get_db),current_user: User = Depends(auth_service.get_current_user),
):
    """
    The update_contact function updates a contact in the database.
        The function takes an id and a body as input, and returns the updated contact.
        If no contact is found with that id, it raises an HTTPException.
    
    :param body: ContactModel: Get the data from the request body
    :param contact_id: int: Find the contact to update
    :param db: Session: Pass the database session into the function
    :param current_user: User: Get the user_id from the token
    :param : Get the contact id from the path
    :return: A contactmodel object
    :doc-author: Trelent
    """
    contact = await repository_contacts.update(contact_id, body,current_user.id, db)
    if contact is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Not found")
    return contact


@router.patch("/{contact_id}/favorite", response_model=ContactResponse)
async def favorite_update(
    body: ContactFavoriteModel,
    contact_id: int = Path(ge=1),
    db: Session = Depends(get_db),current_user: User = Depends(auth_service.get_current_user),
):
    """
    The favorite_update function updates the favorite status of a contact.
        Args:
            body (ContactFavoriteModel): The updated favorite status of the contact.
            contact_id (int): The id of the contact to update.
    
    :param body: ContactFavoriteModel: Get the data from the request body
    :param contact_id: int: Get the contact id from the path
    :param db: Session: Get the database session
    :param current_user: User: Get the user information from the token
    :param : Get the contact id from the url
    :return: A contactfavoritemodel object
    :doc-author: Trelent
    """
    contact = await repository_contacts.favorite_update(contact_id,current_user.id, body, db)
    if contact is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Not found")
    return contact


@router.delete("/{contact_id}", status_code=status.HTTP_204_NO_CONTENT)
async def remove_contact(contact_id: int = Path(ge=1), db: Session = Depends(get_db),current_user: User = Depends(auth_service.get_current_user),):
    """
    The remove_contact function removes a contact from the database.
        Args:
            contact_id (int): The id of the contact to be removed.
            db (Session, optional): SQLAlchemy Session. Defaults to Depends(get_db).
            current_user (User, optional): User object for authentication purposes. Defaults to Depends(auth_service.get_current_user).
    
    :param contact_id: int: Get the contact id from the url
    :param db: Session: Get the database session
    :param current_user: User: Get the current user from the auth_service
    :param : Specify the contact id
    :return: None, but i want to return the contact that was deleted
    :doc-author: Trelent
    """
    contact = await repository_contacts.delete(contact_id,current_user.id, db)
    if contact is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Not found")
    return None
