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
    """
    Generic service wrapper around CRUD operations.
    """

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
        return self.crud.get(
            db,
            record_id,
        )

    def list(
        self,
        db: Session,
        *,
        skip: int = 0,
        limit: int = 100,
    ) -> list[ModelType]:
        if skip < 0:
            raise ValueError("skip cannot be negative.")

        if limit < 1 or limit > 500:
            raise ValueError(
                "limit must be between 1 and 500."
            )

        return self.crud.get_multi(
            db,
            skip=skip,
            limit=limit,
        )

    def create(
        self,
        db: Session,
        obj_in: CreateSchemaType,
    ) -> ModelType:
        return self.crud.create(
            db,
            obj_in=obj_in,
        )

    def update(
        self,
        db: Session,
        record_id: int,
        obj_in: UpdateSchemaType,
    ) -> ModelType | None:
        db_object = self.crud.get(
            db,
            record_id,
        )

        if db_object is None:
            return None

        return self.crud.update(
            db,
            db_object=db_object,
            obj_in=obj_in,
        )

    def delete(
        self,
        db: Session,
        record_id: int,
    ) -> ModelType | None:
        return self.crud.delete(
            db,
            record_id=record_id,
        )