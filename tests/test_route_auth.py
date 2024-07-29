import pytest
from unittest.mock import MagicMock
from fastapi.testclient import TestClient
from src.services.auth import auth_service
from src.conf import messages
from src.database.models import User

@pytest.fixture
def token(client, user, session, monkeypatch):
    mock_send_email = MagicMock()
    monkeypatch.setattr("src.routes.auth.send_email", mock_send_email)
    client.post("/api/auth/signup", json=user)
    current_user: User = session.query(User).filter(User.email == user.get('email')).first()
    current_user.confirmed = True
    session.commit()
    response = client.post(
        "/api/auth/login",
        data={"username": user.get('email'), "password": user.get('password')},
    )
    data = response.json()
    access_token = data.get("access_token")
    refresh_token = data.get("refresh_token")
    assert access_token is not None
    assert refresh_token is not None
    return access_token, refresh_token

def test_signup(client, user):
    response = client.post("/api/auth/signup", json=user)
    assert response.status_code == 201, response.text
    data = response.json()
    assert data["email"] == user["email"]
    assert "id" in data

def test_signup_existing_user(client, user):
    client.post("/api/auth/signup", json=user)
    response = client.post("/api/auth/signup", json=user)
    assert response.status_code == 409, response.text
    assert response.json()["detail"] == messages.ACCOUNT_EXIST

def test_login_success(client, user, token):
    response = client.post("/api/auth/login", data={"username": user["email"], "password": user["password"]})
    data = response.json()
    assert response.status_code == 200, response.text
    assert data["token_type"] == "bearer"
    assert "access_token" in data
    assert "refresh_token" in data

def test_login_invalid_password(client, user):
    response = client.post("/api/auth/login", data={"username": user["email"], "password": "wrong_password"})
    assert response.status_code == 401, response.text
    assert response.json()["detail"] == messages.INVALID_PASSWORD

def test_login_invalid_email(client, user):
    response = client.post("/api/auth/login", data={"username": "wrong@example.com", "password": user["password"]})
    assert response.status_code == 401, response.text
    assert response.json()["detail"] == messages.INVALID_EMAIL

def test_refresh_token_success(client, token):
    response = client.get("/api/auth/refresh_token", headers={"Authorization": f"Bearer {token[1]}"})
    data = response.json()
    assert response.status_code == 200, response.text
    assert data["token_type"] == "bearer"
    assert "access_token" in data
    assert "refresh_token" in data

def test_refresh_token_invalid(client):
    response = client.get("/api/auth/refresh_token", headers={"Authorization": "Bearer invalid_token"})
    assert response.status_code == 401, response.text
    assert response.json()["detail"] == messages.INVALID_REFRESH_TOKEN

def test_refresh_token_no_token(client):
    response = client.get("/api/auth/refresh_token")
    assert response.status_code == 401, response.text
    assert response.json()["detail"] == "Not authenticated"

if __name__ == "__main__":
    pytest.main()
