import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from main import app
from src.database.models import Base
from src.database.db import get_db

SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

@pytest.fixture(scope="module")
def session():
    # Create the database

    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)

    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()
        
@pytest.fixture(scope="module")
def client(session):
    # Dependency override

    def override_get_db():
        try:
            yield session
        finally:
            session.close()

    app.dependency_overrides[get_db] = override_get_db


    yield TestClient(app)
    
@pytest.fixture(scope="module")
def user():
    return {
        "username": "Borys",
        "email": "borys@example.com",
        "password": "qwerty",
        "avatar": None,
        "role": "user",
    }


@pytest.fixture(scope="module")
def contact():
    result = {
        "first_name": "aaaa",
        "last_name": "bbbbb",
        "email": "aaa@uu.cc",
        "phone": None,
        "birthday": None,
        "comments": None,
        "favorite": False,
        "user_id": 1,
    }
    return result
        
