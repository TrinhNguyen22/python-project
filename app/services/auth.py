

from datetime import timedelta, datetime
from typing import Optional
from uuid import UUID

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from app.database import get_db_context
from app.settings import JWT_ALGORITHM, JWT_SECRET
from sqlalchemy.orm import Session
from app.schemas.user import User, verify_password
from jose import JWTError, jwt


oa2_bearer = OAuth2PasswordBearer(tokenUrl='/auth/token')


def authenticate_user(
    username: str,
    password: str,
    db: Session = Depends(get_db_context)
):
    user = db.query(User).filter(User.username == username).first()
    if not user:
        return False
    if not verify_password(password, user.hashed_password):
        return False
    return user


def create_access_token(
        subject: User,
        expires_delta: Optional[timedelta] = None
) -> str:
    claims = {
        'sub': subject.username,
        'id': str(subject.id),
        'first_name': subject.first_name,
        'last_name': subject.last_name,
        'is_admin': subject.is_admin
    }
    expire = datetime.utcnow() + expires_delta \
        if expires_delta else datetime.utcnow() + timedelta(minutes=20)
    claims.update({"exp": expire, "sub": str(subject.username)})
    return jwt.encode(claims, JWT_SECRET, algorithm=JWT_ALGORITHM)


def token_interceptor(token: str = Depends(oa2_bearer)) -> User:
    try:
        payload = jwt.decode(token, JWT_SECRET, algorithms=[JWT_ALGORITHM])
        user = User()
        user.username = payload.get('sub')
        user.id = payload.get('id')
        user.first_name = payload.get('first_name')
        user.last_name = payload.get('last_name')
        user.is_admin = payload.get('is_admin')

        if user.username is None or user.id is None:
            raise token_exception()
        return user
    except JWTError:
        raise token_exception()


def token_exception() -> HTTPException:
    return HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail='Invalid credential',
        headers={'WWW-Authenticate': 'bearer'}
    )


def get_current_user(
    token: str = Depends(oa2_bearer),
    db: Session = Depends(get_db_context),
) -> User:
    """Decode JWT and return the authenticated user object."""
    try:
        payload = jwt.decode(
            token,
            JWT_SECRET,
            algorithms=[JWT_ALGORITHM],
        )
        user_id: UUID | None = payload.get('id')
        if user_id is None:
            raise token_exception()
    except JWTError:
        raise token_exception()

    user = db.get(User, user_id)
    if not user or not user.is_active:
        raise token_exception()
    return user
