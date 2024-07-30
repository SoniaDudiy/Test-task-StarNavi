import unittest
from unittest.mock import AsyncMock, MagicMock
from sqlalchemy.orm import Session
from src.database.models import User
from src.schemas import UserModel
from src.repository.users import create_user, get_user_by_email, update_token

class TestUser(unittest.TestCase):
    def setUp(self):
        self.session = AsyncMock(spec=Session)
        self.body = UserModel(username="username", email="username@test.ua", password="12345678")
        self.user = User(username="username", email="username@test.ua", password="12345678", refresh_token="token", confirmed=False)

    async def test_create_user(self):
        body = self.body
        db = self.session
        result = await create_user(body, db)
        self.assertIsNotNone(result)
        self.assertEqual(result.username, body.username)
        self.assertEqual(result.email, body.email)

    async def test_get_user_by_email(self):
        email = self.user.email
        db = self.session
        db.execute.return_value.scalars.return_value.first.return_value = self.user
        result = await get_user_by_email(email, db)
        self.assertIsNotNone(result)
        self.assertEqual(result.email, email)

    async def test_update_token(self):
        user = self.user
        db = self.session
        token = user.refresh_token
        result = await update_token(user, token, db)
        self.assertIsNotNone(result)
        self.assertEqual(result.refresh_token, token)

if __name__ == "__main__":
    unittest.main()
