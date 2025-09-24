from uuid import UUID
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.orm import Session
from typing import List, Optional

from database import get_db_context
from schemas.task import Task
from schemas.user import User
from models.task import TaskCreate, TaskViewModel, TaskUpdate
from services import auth as auth_service

router = APIRouter(prefix="/tasks", tags=["Tasks"])


def get_tasks(
    db: Session = Depends(get_db_context),
    owner_id: Optional[UUID] = None,
    status: Optional[str] = None,
    priority: Optional[int] = None,
    skip: int = 0,
    limit: int = 100,
) -> List[TaskViewModel]:
    query = select(Task)
    if owner_id is not None:
        query = query.where(Task.owner_id == owner_id)
    if status is not None:
        query = query.where(Task.status == status)
    if priority is not None:
        query = query.where(Task.priority == priority)
    return db.execute(query.offset(skip).limit(limit)).scalars().all()


@router.get("", response_model=List[TaskViewModel],
            status_code=status.HTTP_200_OK)
def list_tasks(
    status_: str | None = None,
    priority: int | None = None,
    db: Session = Depends(get_db_context),
    user: User = Depends(auth_service.token_interceptor),
    current_user: User = Depends(auth_service.get_current_user)
):
    # Admin sees all; user sees own
    owner_id = None if current_user.is_admin else current_user.id
    return get_tasks(db, owner_id=owner_id, status=status_, priority=priority)


@router.post("", response_model=TaskViewModel,
             status_code=status.HTTP_201_CREATED)
def create_task(
    task_in: TaskCreate,
    db: Session = Depends(get_db_context),
    user: User = Depends(auth_service.token_interceptor),
    current_user: User = Depends(auth_service.get_current_user),
):
    db_task = Task(
        summary=task_in.summary,
        description=task_in.description,
        status=task_in.status,
        priority=task_in.priority,
        owner_id=current_user.id,
    )
    db.add(db_task)
    db.commit()
    db.refresh(db_task)
    return db_task


@router.get("/{task_id}",
            response_model=TaskViewModel, status_code=status.HTTP_200_OK)
def get_task(
    task_id: UUID,
    db: Session = Depends(get_db_context),
    user: User = Depends(auth_service.token_interceptor),
    current_user: User = Depends(auth_service.get_current_user),
):
    task = db.get(Task, task_id)
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    if not current_user.is_admin and task.owner_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not authorized")
    return task


@router.put("/{task_id}",
            response_model=TaskViewModel, status_code=status.HTTP_200_OK)
def update_task(
    task_id: UUID,
    task_in: TaskUpdate,
    db: Session = Depends(get_db_context),
    user: User = Depends(auth_service.token_interceptor),
    current_user: User = Depends(auth_service.get_current_user),
):
    db_task = db.get(Task, task_id)
    if not db_task:
        raise HTTPException(status_code=404, detail="Task not found")
    if not current_user.is_admin and db_task.owner_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not authorized")
    update_data = task_in.dict(exclude_unset=True)
    for field, value in update_data.items():
        setattr(db_task, field, value)
    db.add(db_task)
    db.commit()
    db.refresh(db_task)
    return db_task


@router.delete("/{task_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_task(
    task_id: UUID,
    db: Session = Depends(get_db_context),
    user: User = Depends(auth_service.token_interceptor),
    current_user: User = Depends(auth_service.get_current_user),
):
    db_task = db.get(Task, task_id)
    if not db_task:
        raise HTTPException(status_code=404, detail="Task not found")
    if not current_user.is_admin and db_task.owner_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not authorized")
    db.delete(db_task)
    db.commit()
