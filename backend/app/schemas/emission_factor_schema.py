from datetime import datetime

from pydantic import Field

from app.schemas.base import ORMBaseModel


class EmissionFactorCreate(ORMBaseModel):
    source: str = Field(
        min_length=2,
        max_length=100,
    )

    category: str = Field(
        min_length=2,
        max_length=100,
    )

    factor: float = Field(
        gt=0,
    )

    unit: str = Field(
        min_length=1,
        max_length=30,
    )

    status: bool = True


class EmissionFactorUpdate(ORMBaseModel):
    source: str | None = Field(
        default=None,
        min_length=2,
        max_length=100,
    )

    category: str | None = Field(
        default=None,
        min_length=2,
        max_length=100,
    )

    factor: float | None = Field(
        default=None,
        gt=0,
    )

    unit: str | None = Field(
        default=None,
        min_length=1,
        max_length=30,
    )

    status: bool | None = None


class EmissionFactorResponse(ORMBaseModel):
    id: int
    source: str
    category: str
    factor: float
    unit: str
    status: bool
    created_at: datetime | None = None
    updated_at: datetime | None = None