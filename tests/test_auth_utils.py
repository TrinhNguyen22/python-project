import os
from datetime import timedelta

import pytest
from jose import jwt

from app.schemas.user import User, hash_password, verify_password
from app.services import auth as auth_service


def test_hash_and_verify_password_roundtrip():
    plain = "S3cret!Pass"
    hashed = hash_password(plain)
    assert hashed != plain
    assert verify_password(plain, hashed) is True
    assert verify_password("wrong", hashed) is False


@pytest.mark.parametrize("minutes", [1, 30])
def test_create_access_token_contains_expected_claims(minutes):
    # Ensure JWT settings exist
    assert os.getenv("JWT_SECRET")
    assert os.getenv("JWT_ALGORITHM")

    user = User()
    user.id = "00000000-0000-0000-0000-000000000001"
    user.username = "jwt_tester"
    user.first_name = "Jwt"
    user.last_name = "Tester"
    user.is_admin = False

    token = auth_service.create_access_token(
        subject=user,
        expires_delta=timedelta(minutes=minutes),
    )

    decoded = jwt.get_unverified_claims(token)
    # core claims
    assert decoded["sub"] == user.username
    assert decoded["id"] == str(user.id)
    # presence of exp
    assert "exp" in decoded


def test_get_current_user_success(db_session):
    # Arrange: create a real user in DB
    db_user = User(
        email="jwt_success@example.com",
        username="jwt_success",
        first_name="Jwt",
        last_name="Success",
        hashed_password=hash_password("Password01"),
        is_active=True,
        is_admin=False,
    )
    db_session.add(db_user)
    db_session.commit()
    db_session.refresh(db_user)

    token = auth_service.create_access_token(db_user, timedelta(minutes=5))

    # Act
    current = auth_service.get_current_user(
        token=token, db=db_session
    )

    # Assert
    assert current.id == db_user.id
    assert current.username == db_user.username


def test_get_current_user_invalid_token_raises():
    with pytest.raises(Exception):
        auth_service.get_current_user(
            token="invalid.token.value", db=None  # db unused when decode fails
        )


