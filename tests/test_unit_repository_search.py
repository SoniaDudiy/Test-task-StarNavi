import pytest
from unittest.mock import AsyncMock
from sqlalchemy.ext.asyncio import AsyncSession
from src.repository.users import get_user_by_email, create_user, update_token
from src.schemas import UserModel
from src.database.models import User

@pytest.mark.asyncio
async def test_get_user_by_email(session: AsyncSession):
    # Mocking the database query
    mock_query = AsyncMock()
    mock_query.execute.return_value.scalars.return_value.first.return_value = User(
        id=1, email="test@example.com", username="testuser", password="hashedpassword"
    )
    session.execute = mock_query.execute

    # Test the function
    email = "test@example.com"
    user = await get_user_by_email(email, session)
    assert user.email == email

@pytest.mark.asyncio
async def test_create_user(session: AsyncSession):
    # Create a mock for Gravatar
    mock_gravatar = AsyncMock()
    mock_gravatar.get_image.return_value = "https://example.com/avatar.png"

    # Mock the Gravatar class
    with pytest.MonkeyPatch.context() as monkeypatch:
        monkeypatch.setattr("libgravatar.Gravatar", mock_gravatar)

        # Prepare UserModel
        user_model = UserModel(
            username="newuser",
            email="newuser@example.com",
            password="newpassword"
        )

        # Mocking the session methods
        session.add = AsyncMock()
        session.commit = AsyncMock()
        session.refresh = AsyncMock()

        user = await create_user(user_model, session)

        # Assertions
        assert user.email == user_model.email
        assert user.avatar == "https://example.com/avatar.png"

@pytest.mark.asyncio
async def test_update_token(session: AsyncSession):
    # Mock a User instance
    user = User(id=1, email="test@example.com", username="testuser", password="hashedpassword")

    # Mock the session methods
    session.add = AsyncMock()
    session.commit = AsyncMock()
    session.refresh = AsyncMock()

    # Call update_token
    refresh_token = "new_refresh_token"
    await update_token(user, refresh_token, session)

    # Assertions
    assert user.refresh_token == refresh_token
    session.add.assert_called_once_with(user)
    session.commit.assert_called_once()

