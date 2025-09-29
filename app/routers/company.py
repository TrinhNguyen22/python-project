from typing import List, Optional
from uuid import UUID
from app.database import get_db_context
from fastapi import APIRouter, Depends, HTTPException
from app.models.company import CompanyCreate, CompanyUpdate, CompanyViewModel
from app.schemas.company import Company
from app.schemas.user import User
from app.services import auth as auth_service
from starlette import status
from sqlalchemy.orm import Session

router = APIRouter(prefix='/companies', tags=['Companies'])


@router.get('/', status_code=status.HTTP_200_OK,
            response_model=List[CompanyViewModel])
def get_companies(
    db: Session = Depends(get_db_context),
    skip: int = 0,
    limit: int = 100,
    mode: Optional[str] = None,
    rating: Optional[float] = None
):
    q = db.query(Company)
    if mode:
        q = q.filter(Company.mode == mode)
    if rating is not None:
        q = q.filter(Company.rating >= rating)
    return q.offset(skip).limit(limit).all()


@router.get('/{company_id}', status_code=status.HTTP_200_OK,
            response_model=CompanyViewModel)
async def get_company(
    company_id: UUID,
    db: Session = Depends(get_db_context)
):
    return db.query(Company).filter(Company.id == company_id).first()


@router.post('/', status_code=status.HTTP_201_CREATED)
async def create_company(
    company_in: CompanyCreate,
    db: Session = Depends(get_db_context),
    user: User = Depends(auth_service.token_interceptor)
) -> CompanyViewModel:
    db_company = Company(
        name=company_in.name,
        description=company_in.description,
        mode=company_in.mode,
        rating=company_in.rating
    )
    db.add(db_company)
    db.commit()
    db.refresh(db_company)
    return db_company


@router.put("/{company_id}", response_model=CompanyViewModel,
            status_code=status.HTTP_200_OK)
def update_company(
    company_id: UUID,
    company_in: CompanyUpdate,
    db: Session = Depends(get_db_context),
    user: User = Depends(auth_service.token_interceptor)
):
    db_company = db.get(Company, company_id)
    if not db_company:
        raise HTTPException(status_code=404, detail="Company not found")
    update_data = company_in.dict(exclude_unset=True)
    for field, value in update_data.items():
        setattr(db_company, field, value)
    db.add(db_company)
    db.commit()
    db.refresh(db_company)
    return db_company


@router.delete("/{company_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_company(
    company_id: UUID,
    db: Session = Depends(get_db_context),
    user: User = Depends(auth_service.token_interceptor)
):
    db_company = db.get(Company, company_id)
    if not db_company:
        raise HTTPException(status_code=404, detail="Company not found")
    db.delete(db_company)
    db.commit()
