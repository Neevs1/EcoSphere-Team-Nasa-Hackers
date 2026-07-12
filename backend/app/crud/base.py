from typing import Any, Generic, TypeVar

from pydantic import BaseModel
from sqlalchemy import select, func as sa_func, or_
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

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


class CRUDBase(
    Generic[
        ModelType,
        CreateSchemaType,
        UpdateSchemaType,
    ]
):
    """
    Generic CRUD class with search, status filtering, and soft delete.
    """

    def __init__(
        self,
        model: type[ModelType],
    ):
        self.model = model

    def get(
        self,
        db: Session,
        record_id: int,
    ) -> ModelType | None:
        return db.get(
            self.model,
            record_id,
        )

    def _build_list_statement(
        self,
        search: str | None = None,
        status_filter: str | None = None,
    ):
        stmt = select(self.model)

        if search and hasattr(self.model, "name"):
            stmt = stmt.where(self.model.name.ilike(f"%{search}%"))
            
        if status_filter is not None and hasattr(self.model, "status"):
            if isinstance(self.model.status.type.python_type, type(bool)):
                is_active = status_filter.lower() == "active"
                stmt = stmt.where(self.model.status == is_active)
            else:
                stmt = stmt.where(self.model.status == status_filter)
                
        return stmt

    def get_multi(
        self,
        db: Session,
        *,
        skip: int = 0,
        limit: int = 100,
        search: str | None = None,
        status_filter: str | None = None,
    ) -> list[ModelType]:
        stmt = self._build_list_statement(search, status_filter)
        if hasattr(self.model, "id"):
            stmt = stmt.order_by(self.model.id.desc())
        stmt = stmt.offset(skip).limit(limit)
        return list(db.scalars(stmt).all())

    def count(
        self,
        db: Session,
        search: str | None = None,
        status_filter: str | None = None,
    ) -> int:
        stmt = self._build_list_statement(search, status_filter)
        count_stmt = select(sa_func.count()).select_from(stmt.subquery())
        return db.scalar(count_stmt) or 0

    def create(
        self,
        db: Session,
        *,
        obj_in: CreateSchemaType,
    ) -> ModelType:
        object_data = obj_in.model_dump()
        db_object = self.model(**object_data)

        try:
            db.add(db_object)
            db.commit()
            db.refresh(db_object)
            return db_object
        except Exception:
            db.rollback()
            raise

    def update(
        self,
        db: Session,
        *,
        db_object: ModelType,
        obj_in: UpdateSchemaType | dict[str, Any],
    ) -> ModelType:
        if isinstance(obj_in, dict):
            update_data = obj_in
        else:
            update_data = obj_in.model_dump(exclude_unset=True)

        for field_name, value in update_data.items():
            if hasattr(db_object, field_name):
                setattr(db_object, field_name, value)

        try:
            db.add(db_object)
            db.commit()
            db.refresh(db_object)
            return db_object
        except Exception:
            db.rollback()
            raise

    def delete(
        self,
        db: Session,
        *,
        record_id: int,
    ) -> ModelType | None:
        db_object = self.get(db, record_id)
        if db_object is None:
            return None

        try:
            if hasattr(self.model, "status") and isinstance(self.model.status.type.python_type, type(bool)):
                # Soft delete
                db_object.status = False
                db.commit()
            else:
                # Hard delete
                db.delete(db_object)
                db.commit()
            return db_object
        except IntegrityError:
            db.rollback()
            raise
        except Exception:
            db.rollback()
            raise