from uuid import UUID
from pydantic import BaseModel, ConfigDict
from typing import Optional


class TaskBase(BaseModel):
    summary: str
    description: Optional[str] = None
    status: Optional[str] = "TODO"
    priority: Optional[int] = 3


class TaskCreate(TaskBase):
    owner_id: Optional[UUID] = None


class TaskUpdate(BaseModel):
    summary: Optional[str] = None
    description: Optional[str] = None
    status: Optional[str] = None
    priority: Optional[int] = None
    owner_id: Optional[UUID] = None


class TaskViewModel(TaskBase):
    id: UUID
    owner_id: Optional[UUID]

    class Config:
        model_config = ConfigDict(from_attributes=True)
