from app.database import Base
from .base_entity import BaseEntity
from sqlalchemy import Column, ForeignKey, Integer, String, Uuid
from sqlalchemy.orm import relationship


class Task(Base, BaseEntity):
    __tablename__ = 'task'

    summary = Column(String, index=True, nullable=False)
    description = Column(String, nullable=True)
    status = Column(String, index=True, default="todo")
    priority = Column(Integer, index=True, default=3)
    owner_id = Column(Uuid, ForeignKey("user.id"), nullable=True)

    owner = relationship("User", back_populates="tasks")
