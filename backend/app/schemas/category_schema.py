from datetime import datetime
from typing import Literal

from pydantic import Field

from app.schemas.base import ORMBaseModel


CategoryType = Literal[
    "CSR Activity",
    "Challenge",
]


class CategoryCreate(ORMBaseModel):
    name: str = Field(
        min_length=2,
        max_length=100,
    )

    type: CategoryType

    status: bool = True


class CategoryUpdate(ORMBaseModel):
    name: str | None = Field(
        default=None,
        min_length=2,
        max_length=100,
    )

    type: CategoryType | None = None

    status: bool | None = None


class CategoryResponse(ORMBaseModel):
    id: int
    name: str
    type: str
    status: bool
    created_at: datetime | None = None
    updated_at: datetime | None = None
