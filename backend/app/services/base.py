from typing import Generic, TypeVar

from pydantic import BaseModel
from sqlalchemy.orm import Session

from app.crud.base import CRUDBase
from app.database.base import Base


ModelType = TypeVar(
    "ModelType",
    bound=Base,
)

CreateSchemaType = TypeVar(
    "CreateSchemaType",
    bound=BaseModel,
)

UpdateSchemaType = TypeVar(
    "UpdateSchemaType",
    bound=BaseModel,
)


class BaseService(
    Generic[
        ModelType,
        CreateSchemaType,
        UpdateSchemaType,
    ]
):
    def __init__(
        self,
        crud: CRUDBase[
            ModelType,
            CreateSchemaType,
            UpdateSchemaType,
        ],
    ):
        self.crud = crud

    def get(
        self,
        db: Session,
        record_id: int,
    ) -> ModelType | None:
        return self.crud.get(db, record_id)

    def list(
        self,
        db: Session,
        *,
        page: int = 1,
        page_size: int = 100,
        search: str | None = None,
        status_filter: str | None = None,
    ) -> dict:
        if page < 1:
            raise ValueError("page must be >= 1.")
        if page_size < 1 or page_size > 500:
            raise ValueError("page_size must be between 1 and 500.")

        skip = (page - 1) * page_size
        items = self.crud.get_multi(
            db, skip=skip, limit=page_size, search=search, status_filter=status_filter
        )
        total = self.crud.count(db, search=search, status_filter=status_filter)
        
        import math
        total_pages = max(1, math.ceil(total / page_size))

        return {
            "items": items,
            "total": total,
            "page": page,
            "page_size": page_size,
            "total_pages": total_pages,
        }

    def create(
        self,
        db: Session,
        obj_in: CreateSchemaType,
    ) -> ModelType:
        return self.crud.create(db, obj_in=obj_in)

    def update(
        self,
        db: Session,
        record_id: int,
        obj_in: UpdateSchemaType,
    ) -> ModelType | None:
        db_object = self.crud.get(db, record_id)
        if db_object is None:
            return None
        return self.crud.update(db, db_object=db_object, obj_in=obj_in)

    def delete(
        self,
        db: Session,
        record_id: int,
    ) -> ModelType | None:
        return self.crud.delete(db, record_id=record_id)