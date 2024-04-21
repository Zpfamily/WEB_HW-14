import unittest
from unittest.mock import MagicMock

from datetime import date, timedelta

from sqlalchemy.orm import Session
from sqlalchemy import select, text, extract, desc
from pathlib import Path
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from src.schemas import ContactModel,ContactFavoriteModel
from src.database.models import Contact, User



from src.repository.contacts import (
    # get_contacts,
    get_contact_by_id,
    get_contact_by_email,
    create,
    update,
    favorite_update,
    delete
)

class TestContactsRepository (unittest.IsolatedAsyncioTestCase):
    def setUp(self):
        self.session = MagicMock(spec=Session)
        self.user = User(id = 1, email = "user@example.com")
        
    # async def test_get_contacts(self):
    #     contact = [Contact(), Contact(), Contact()]
    #     favorite = True
    #     q = self.session.query().filter_by()
    #     if favorite is not None:
    #         q = q.filter_by()
    #     q.offset().limit().all.return_value = contact
        
    #     result = await get_contacts(skip=0, limit=10, user_id=self.user.id, db=self.session)
    #     self.assertEqual(result, contact)
        
    async def test_get_contact_found_by_id(self):
        contact = Contact()
        self.session.query().filter_by().first.return_value = contact
        result = await get_contact_by_id(contact_id=1, user_id=self.user.id, db=self.session)  # type: ignore
        self.assertEqual(result, contact)
        
    async def test_get_contact_found_by_email(self):
        contact = Contact()
        self.session.query().filter_by().first.return_value = contact
        result = await get_contact_by_email(email="as@ee.ua", user_id=self.user.id, db=self.session)  # type: ignore
        self.assertEqual(result, contact)
        
    async def test_get_contact_not_found_by_id(self):
        self.session.query().filter_by().first.return_value = None
        result = await get_contact_by_id(contact_id=1, user_id=self.user.id, db=self.session)  # type: ignore
        self.assertIsNone(result)
        
    async def test_get_contact_not_found_by_email(self):
        self.session.query().filter_by().first.return_value = None
        result = await get_contact_by_email(email="as@ee.ua", user_id=self.user.id, db=self.session)  # type: ignore
        self.assertIsNone(result)
        
    async def test_create_contact(self):
        body = ContactModel(first_name="test1", last_name="test2", email="aa@uu.uu", phone="+380 (44) 1234567")
        result = await create(body=body, user_id=self.user.id, db=self.session)  # type: ignore
        self.assertEqual(result.first_name, body.first_name)
        self.assertEqual(result.last_name, body.last_name)
        self.assertEqual(result.email, body.email)
        self.assertEqual(result.phone, body.phone)
        self.assertTrue(hasattr(result, "id"))
        self.assertEqual(result.user_id, self.user.id)
        
    async def test_remove_contact_found(self):
        contact = Contact()
        self.session.query().filter_by().first.return_value = contact
        result = await delete(contact_id=1, user_id=self.user.id, db=self.session)  # type: ignore
        self.assertEqual(result, contact)

    async def test_remove_contact_not_found(self):
        self.session.query().filter_by().first.return_value = None
        result = await delete(contact_id=1, user_id=self.user.id, db=self.session)  # type: ignore
        self.assertIsNone(result)
        
    async def test_update_contact_found(self):
        contact = Contact()
        body = ContactModel(first_name="test1-1", last_name="test2-1", email="aa@uu.uu", phone="+380 (44) 1234567")
        self.session.query().filter_by().first.return_value = contact
        self.session.commit.return_value = None
        result = await update(contact_id=1, body=body, user_id=self.user.id, db=self.session)  # type: ignore
        self.assertEqual(result, contact)

    async def test_update_contact_not_found(self):
        body = ContactModel(first_name="test1-1", last_name="test2-1", email="aa@uu.uu", phone="+380 (44) 1234567")
        self.session.query().filter_by().first.return_value = None
        self.session.commit.return_value = None
        result = await update(contact_id=1, body=body, user_id=self.user.id, db=self.session)  # type: ignore
        self.assertIsNone(result)
        
    async def test_update_favorite_contact_found(self):
        body = ContactFavoriteModel(favorite=True)
        contact = Contact()
        self.session.query().filter_by().first.return_value = contact
        result = await favorite_update(contact_id=1, body=body, user_id=self.user.id, db=self.session)  # type: ignore
        self.assertEqual(result, contact)

    async def test_update_favorite_contact_not_found(self):
        body = ContactFavoriteModel(favorite=True)
        contact = Contact()
        self.session.query().filter_by().first.return_value = None
        result = await favorite_update(contact_id=1, body=body, user_id=self.user.id, db=self.session)  # type: ignore
        self.assertIsNone(result)
        

if __name__ == '__main__':
    unittest.main()