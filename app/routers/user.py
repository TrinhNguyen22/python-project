from typing import List
from uuid import UUID

from models.user import UserCreate, UserUpdate, UserViewModel
from database import get_db_context
from fastapi import APIRouter, Depends, HTTPException
from schemas.user import User, hash_password
from starlette import status
from sqlalchemy.orm import Session
from services import auth as auth_service

router = APIRouter(prefix='/users', tags=['Users'])


@router.get('', response_model=List[UserViewModel],
            status_code=status.HTTP_200_OK)
async def get_users(
    db: Session = Depends(get_db_context),
    user: User = Depends(auth_service.token_interceptor)
):
    return db.query(User).all()


@router.get('/{user_id}', response_model=UserViewModel,
            status_code=status.HTTP_200_OK)
def get_user_by_id(
    user_id: UUID,
    db: Session = Depends(get_db_context),
    user: User = Depends(auth_service.token_interceptor)
):
    return db.query(User).filter(User.id == user_id).first()


@router.post('', status_code=status.HTTP_201_CREATED)
async def create_user(
    request: UserCreate,
    db: Session = Depends(get_db_context),
    user: User = Depends(auth_service.token_interceptor)
) -> UserViewModel:
    hashed = hash_password(request.password)
    db_obj = User(
        email=request.email,
        username=request.username,
        first_name=request.first_name,
        last_name=request.last_name,
        hashed_password=hashed,
        company_id=request.company_id
    )
    db.add(db_obj)
    db.commit()
    db.refresh(db_obj)
    return db_obj


@router.put("/{user_id}", response_model=UserViewModel)
def update_user(
    user_id: UUID,
    user_in: UserUpdate,
    db: Session = Depends(get_db_context),
    user: User = Depends(auth_service.token_interceptor),
    current_user: User = Depends(auth_service.get_current_user),
):
    db_user = db.get(User, user_id)
    if not db_user:
        raise HTTPException(status_code=404, detail="User not found")
    # Only admin or the user themself can update
    if not current_user.is_admin and current_user.id != db_user.id:
        raise HTTPException(status_code=403, detail="Not authorized")
    update_data = user_in.dict(exclude_unset=True)
    for field, value in update_data.items():
        setattr(db_user, field, value)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


@router.delete("/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_user(
    user_id: UUID,
    db: Session = Depends(get_db_context),
    user: User = Depends(auth_service.token_interceptor),
    current_user: User = Depends(auth_service.get_current_user),
):
    # Only admin can delete
    db_user = db.get(User, user_id)
    if not db_user:
        raise HTTPException(status_code=404, detail="User not found")
    db.delete(db_user)
    db.commit()
