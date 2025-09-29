from fastapi.testclient import TestClient
import pytest
from sqlalchemy.orm import Session
from app.schemas.user import User, hash_password


@pytest.fixture
def create_test_user(db_session: Session):
    username = "auth_tester"
    existing = db_session.query(User).filter(User.username == username).first()
    if not existing:
        user = User(
            email="auth_tester@example.com",
            username=username,
            first_name="Auth",
            last_name="Tester",
            hashed_password=hash_password("testpass"),
            is_active=True,
            is_admin=False,
        )
        db_session.add(user)
        db_session.commit()
        db_session.refresh(user)
        return user
    return existing


def test_login_success(client: TestClient, create_test_user):
    response = client.post(
        "/auth/token",
        data={"username": create_test_user.username, "password": "testpass"},
        headers={"Content-Type": "application/x-www-form-urlencoded"},
    )
    assert response.status_code == 200
    body = response.json()
    assert "access_token" in body
    assert body["token_type"] == "bearer"

    global access_token
    access_token = body["access_token"]


def test_login_invalid_password(client: TestClient, create_test_user):
    r = client.post(
        "/auth/token",
        data={
            "username": create_test_user.username,
            "password": "wrongpass"
        },
        headers={"Content-Type": "application/x-www-form-urlencoded"},
    )
    assert r.status_code == 401
    assert r.json()["detail"].lower().find("invalid") >= 0 or \
        r.json()["detail"].lower().find("credential") >= 0


def test_login_nonexistent_user(client: TestClient):
    r = client.post(
        "/auth/token",
        data={"username": "no_such_user", "password": "whatever"},
        headers={"Content-Type": "application/x-www-form-urlencoded"},
    )
    assert r.status_code == 401
