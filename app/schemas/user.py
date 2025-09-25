from passlib.context import CryptContext
from sqlalchemy import Boolean, Column, ForeignKey, String, Uuid
from sqlalchemy.orm import relationship

from app.database import Base
from app.schemas.base_entity import BaseEntity

pwd_context = CryptContext(schemes=['bcrypt'])


class User(Base, BaseEntity):
    __tablename__ = 'user'

    email = Column(String, unique=True, index=True, nullable=False)
    username = Column(String, unique=True, index=True, nullable=False)
    first_name = Column(String, nullable=True)
    last_name = Column(String, nullable=True)
    hashed_password = Column(String, nullable=False)
    is_active = Column(Boolean, default=True)
    is_admin = Column(Boolean, default=False)

    company_id = Column(Uuid, ForeignKey("company.id"), nullable=True)

    company = relationship("Company", back_populates="users")

    tasks = relationship("Task", back_populates="owner")


def hash_password(password: str) -> str:
    return pwd_context.hash(password)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)
