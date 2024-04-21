from typing import List
import sys
import os

from fastapi import Path, Depends, HTTPException, Query, status, APIRouter
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session
import pytest

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from src.database.db import get_db
from src.schemas import ContactFavoriteModel, ContactModel, ContactResponse
from src.repository import contacts as repository_contacts
from src.services.auth import auth_service
from src.database.models import User
from fastapi_limiter.depends import RateLimiter
from unittest.mock import MagicMock,patch

def create_user(client, session, user, monkeypatch):
    mock_send_email = MagicMock()
    monkeypatch.setattr("src.services.emails.send_email", mock_send_email)

    response = client.post(
        "/api/auth/signup",
        json=user,
    )
    current_user: User = session.query(User).filter(User.email == user.get("email")).first()
    current_user.confirmed = True
    session.commit()
    
def get_access_token_user(client, user):
    response = client.post(
        "/api/auth/login",
        data={"username": user.get("email"), "password": user.get("password")},
    )
    data = response.json()
    access_token = data["access_token"]
    return f"Bearer {access_token}"

@pytest.fixture()
def token(client, user, session, monkeypatch, mock_ratelimiter):
    """ get auth token foa all auth requests
        mock_ratelimiter not used, but required in argumants for execute fixture before
    """
    # print(f"token {db.redis_pool=}")
    create_user(client, session, user, monkeypatch)
    return get_access_token_user(client, user)

@pytest.fixture()
def token(client, user, session, monkeypatch, mock_ratelimiter):
    """ get auth token foa all auth requests
        mock_ratelimiter not used, but required in argumants for execute fixture before
    """
    # print(f"token {db.redis_pool=}")
    create_user(client, session, user, monkeypatch)
    return get_access_token_user(client, user)
    
@pytest.fixture()
def test_create_contact(client, contact, token):
    response = client.post("/api/contacts", json=contact, headers={"Authorization": token})
    assert response.status_code == 201, response.text
    data = response.json()
    assert data["first_name"] == contact.get("first_name")
    assert "id" in data
    
@pytest.fixture()
def test_get_contact(client, token, contact):
    # with patch("src.database.db.redis_pool", False):
    response = client.get("/api/contacts/1", headers={"Authorization": token})
    assert response.status_code == 200, response.text
    data = response.json()
    assert data["first_name"] == contact.get("first_name")
    assert "id" in data
    
    
@pytest.fixture()    
def test_update_contact(client, token):
    # with patch("src.database.db.redis_pool", False):
    response = client.put("/api/contacts/1", json={"email": "new@email.com"}, headers={"Authorization": token})
    assert response.status_code == 200, response.text
    data = response.json()
    assert data["email"] == "new@email.com"
    assert "id" in data
 
    
@pytest.fixture()    
def test_update_contact_not_found(client, token):
    # with patch("src.database.db.redis_pool", False):
    response = client.put("/api/contacts/2", json={"email": "new@email.com"}, headers={"Authorization": token})
    assert response.status_code == 404, response.text
    data = response.json()
    assert data["detail"] == "Not found"


    
@pytest.fixture()
def test_delete_contact(client, token):
    # with patch("src.database.db.redis_pool", False):
    response = client.delete("/api/contacts/1", headers={"Authorization": token})
    assert response.status_code == 204, response.text


    
@pytest.fixture()
def test_repeat_delete_contact(client, token):
    response = client.delete("/api/contacts/1", headers={"Authorization": token})
    assert response.status_code == 404, response.text
    data = response.json()
    assert data["detail"] == "Not found"