from typing import Any, Generic, TypeVar
from pydantic import BaseModel, create_model

from fastapi import (
    APIRouter,
    Depends,
    HTTPException,
    Query,
    Response,
    status,
)
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app.database.db import get_db
from app.services.base import BaseService
from app.auth.dependencies import require_role

T = TypeVar("T")


def create_paginated_response_model(
    item_schema: type[BaseModel],
    model_name: str
) -> type[BaseModel]:
    return create_model(
        f"Paginated{model_name}Response",
        items=(list[item_schema], ...),
        total=(int, ...),
        page=(int, ...),
        page_size=(int, ...),
        total_pages=(int, ...)
    )


def create_crud_router(
    *,
    service: BaseService,
    create_schema: type[BaseModel],
    update_schema: type[BaseModel],
    response_schema: type[BaseModel],
    prefix: str,
    tag: str,
    resource_name: str,
) -> APIRouter:
    router = APIRouter(
        prefix=prefix,
        tags=[tag],
    )
    
    paginated_response_schema = create_paginated_response_model(
        response_schema, 
        response_schema.__name__
    )

    @router.post(
        "",
        response_model=response_schema,
        status_code=status.HTTP_201_CREATED,
        summary=f"Create {resource_name}",
        dependencies=[Depends(require_role(["system_admin", "esg_admin", "department_head", "compliance_officer"]))],
    )
    def create_record(
        payload: create_schema,
        db: Session = Depends(get_db),
    ) -> Any:
        try:
            return service.create(db, payload)
        except IntegrityError as error:
            db.rollback()
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail=f"{resource_name} could not be created. A unique value may already exist, or a foreign-key reference may be invalid.",
            ) from error
        except ValueError as error:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=str(error),
            ) from error

    @router.get(
        "",
        response_model=paginated_response_schema,
        summary=f"List {resource_name} records",
    )
    def list_records(
        search: str | None = Query(None, description="Search by name"),
        status_filter: str | None = Query(None, alias="status", description="Filter by status (e.g. active/inactive)"),
        page: int = Query(1, ge=1, description="Page number"),
        page_size: int = Query(100, ge=1, le=500, description="Records per page"),
        db: Session = Depends(get_db),
    ) -> Any:
        try:
            return service.list(
                db, page=page, page_size=page_size, search=search, status_filter=status_filter
            )
        except ValueError as error:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=str(error),
            ) from error

    @router.get(
        "/{record_id}",
        response_model=response_schema,
        summary=f"Get {resource_name} by ID",
    )
    def get_record(
        record_id: int,
        db: Session = Depends(get_db),
    ) -> Any:
        record = service.get(db, record_id)
        if record is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"{resource_name} not found.",
            )
        return record

    @router.patch(
        "/{record_id}",
        response_model=response_schema,
        summary=f"Update {resource_name}",
        dependencies=[Depends(require_role(["system_admin", "esg_admin", "department_head", "compliance_officer"]))],
    )
    def update_record(
        record_id: int,
        payload: update_schema,
        db: Session = Depends(get_db),
    ) -> Any:
        try:
            updated_record = service.update(db, record_id, payload)
            if updated_record is None:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail=f"{resource_name} not found.",
                )
            return updated_record
        except HTTPException:
            raise
        except IntegrityError as error:
            db.rollback()
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail=f"{resource_name} could not be updated. A unique value may already exist, or a foreign-key reference may be invalid.",
            ) from error
        except ValueError as error:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=str(error),
            ) from error

    @router.delete(
        "/{record_id}",
        status_code=status.HTTP_204_NO_CONTENT,
        summary=f"Delete {resource_name}",
        dependencies=[Depends(require_role(["system_admin", "esg_admin", "department_head", "compliance_officer"]))],
    )
    def delete_record(
        record_id: int,
        db: Session = Depends(get_db),
    ) -> Response:
        try:
            # Department active children guard
            if resource_name.lower() == "department":
                record = service.get(db, record_id)
                if record:
                    from app.models.user import User
                    from sqlalchemy import select
                    active_users = db.scalar(
                        select(select(User).where(User.department_id == record_id, User.status.is_(True)).exists())
                    )
                    if active_users:
                        raise HTTPException(
                            status_code=status.HTTP_409_CONFLICT,
                            detail="Cannot deactivate a department with active users.",
                        )
                        
            deleted_record = service.delete(db, record_id)
            if deleted_record is None:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail=f"{resource_name} not found.",
                )
            return Response(status_code=status.HTTP_204_NO_CONTENT)
        except HTTPException:
            raise
        except IntegrityError as error:
            db.rollback()
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail=f"{resource_name} cannot be deleted because other records reference it.",
            ) from error

    return router