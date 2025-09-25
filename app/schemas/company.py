from app.database import Base
from .base_entity import BaseEntity
from sqlalchemy import Column, Float, String
from sqlalchemy.orm import relationship


class Company(Base, BaseEntity):
    __tablename__ = 'company'

    name = Column(String, unique=True, index=True, nullable=False)
    description = Column(String, nullable=True)
    mode = Column(String, index=True)
    rating = Column(Float, index=True)

    users = relationship(
        "User",
        back_populates="company",
        cascade="all, delete"
    )
