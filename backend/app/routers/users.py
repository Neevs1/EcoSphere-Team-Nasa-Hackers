from typing import Any
from fastapi import APIRouter, Depends, HTTPException, Query, Response, status
from sqlalchemy.orm import Session
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError

from app.database.db import get_db
from app.models.user import User
from app.schemas.auth_schema import UserCreate, UserUpdate, UserResponse
from app.auth.dependencies import require_role
from app.auth.security import hash_password
from app.routers.base import create_paginated_response_model

users_router = APIRouter(
    prefix="/users",
    tags=["Users"],
)

PaginatedUserResponse = create_paginated_response_model(UserResponse, "User")

@users_router.post(
    "",
    response_model=UserResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Create User",
    dependencies=[Depends(require_role(["system_admin", "esg_admin"]))],
)
def create_user(
    payload: UserCreate,
    db: Session = Depends(get_db),
) -> Any:
    try:
        user_data = payload.model_dump()
        password = user_data.pop("password")
        user_data["password_hash"] = hash_password(password)
        
        user = User(**user_data)
        db.add(user)
        db.commit()
        db.refresh(user)
        return user
    except IntegrityError as error:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="User could not be created. Email might already exist.",
        ) from error

@users_router.get(
    "",
    response_model=PaginatedUserResponse,
    summary="List Users",
    dependencies=[Depends(require_role(["system_admin", "esg_admin", "department_head", "compliance_officer"]))],
)
def list_users(
    search: str | None = Query(None, description="Search by name or email"),
    status_filter: str | None = Query(None, alias="status", description="Filter by status"),
    page: int = Query(1, ge=1),
    page_size: int = Query(100, ge=1, le=500),
    db: Session = Depends(get_db),
) -> Any:
    stmt = select(User)
    
    if search:
        stmt = stmt.where(
            User.name.ilike(f"%{search}%") | User.email.ilike(f"%{search}%")
        )
        
    if status_filter:
        is_active = status_filter.lower() == "active" or status_filter.lower() == "true"
        stmt = stmt.where(User.status == is_active)
        
    from sqlalchemy import func
    total = db.scalar(select(func.count()).select_from(stmt.subquery())) or 0
    
    stmt = stmt.offset((page - 1) * page_size).limit(page_size)
    items = list(db.scalars(stmt).all())
    
    import math
    total_pages = math.ceil(total / page_size) if page_size else 1
    
    return {
        "items": items,
        "total": total,
        "page": page,
        "page_size": page_size,
        "total_pages": total_pages
    }

@users_router.get(
    "/{user_id}",
    response_model=UserResponse,
    summary="Get User by ID",
    dependencies=[Depends(require_role(["system_admin", "esg_admin", "department_head", "compliance_officer"]))],
)
def get_user(
    user_id: int,
    db: Session = Depends(get_db),
) -> Any:
    user = db.get(User, user_id)
    if user is None:
        raise HTTPException(status_code=404, detail="User not found.")
    return user

@users_router.patch(
    "/{user_id}",
    response_model=UserResponse,
    summary="Update User",
    dependencies=[Depends(require_role(["system_admin", "esg_admin"]))],
)
def update_user(
    user_id: int,
    payload: UserUpdate,
    db: Session = Depends(get_db),
) -> Any:
    user = db.get(User, user_id)
    if user is None:
        raise HTTPException(status_code=404, detail="User not found.")
        
    try:
        update_data = payload.model_dump(exclude_unset=True)
        if "password" in update_data:
            password = update_data.pop("password")
            update_data["password_hash"] = hash_password(password)
            
        for key, value in update_data.items():
            setattr(user, key, value)
            
        db.commit()
        db.refresh(user)
        return user
    except IntegrityError as error:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="User could not be updated. Email might already exist.",
        ) from error

@users_router.delete(
    "/{user_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Soft Delete User",
    dependencies=[Depends(require_role(["system_admin", "esg_admin"]))],
)
def delete_user(
    user_id: int,
    db: Session = Depends(get_db),
) -> Response:
    user = db.get(User, user_id)
    if user is None:
        raise HTTPException(status_code=404, detail="User not found.")
        
    user.status = False
    db.commit()
    
    return Response(status_code=status.HTTP_204_NO_CONTENT)
