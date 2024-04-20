import unittest
from unittest.mock import MagicMock

from datetime import date, timedelta

from sqlalchemy.orm import Session
from pathlib import Path
import sys
import os

from src.schemas import ContactModel,ContactFavoriteModel
from src.database.models import Contact, User



from src.repository.contacts import (
    get_contacts,
    get_contact_by_id,
    get_contact_by_email,
    create,
    update,
    favorite_update,
    delete,
    search_birthday,
    search_contacts
)

class TestContactsRepository (unittest.IsolatedAsyncioTestCase):
    def setUp(self):
        self.session = MagicMock(spec=Session)
        self.user = User(id = 1, email = "some@mail.ua")
    async def test_get_contacts(self):
        contact = [Contact(), Contact(), Contact()]
        favorite = True
        q = self.session.query().filter_by()
        if favorite is not None:
            q = q.filter_by()
        q.offset().limit().all.return_value = contact
        result = await get_contacts(skip=0, limit=10, user_id=self.user.id, db=self.session)
        self.assertEqual(result, contact)
        

if __name__ == '__main__':
    unittest.main()