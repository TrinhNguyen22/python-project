from uuid import UUID
from pydantic import BaseModel, ConfigDict
from typing import Optional


class CompanyBase(BaseModel):
    name: str
    description: Optional[str] = None
    mode: Optional[str] = None
    rating: Optional[float] = None


class CompanyCreate(CompanyBase):
    pass


class CompanyUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    mode: Optional[str] = None
    rating: Optional[float] = None


class CompanyViewModel(CompanyBase):
    id: UUID

    class Config:
        model_config = ConfigDict(from_attributes=True)
