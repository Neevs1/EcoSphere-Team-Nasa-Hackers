from datetime import datetime

from pydantic import Field

from app.schemas.base import ORMBaseModel


class ProductESGProfileCreate(ORMBaseModel):
    product_code: str = Field(
        min_length=1,
        max_length=50,
    )

    product_name: str = Field(
        min_length=2,
        max_length=150,
    )

    sustainability_score: float | None = Field(
        default=None,
        ge=0,
        le=100,
    )

    carbon_rating: float | None = Field(
        default=None,
        ge=0,
    )

    recyclable: bool = False


class ProductESGProfileUpdate(ORMBaseModel):
    product_code: str | None = Field(
        default=None,
        min_length=1,
        max_length=50,
    )

    product_name: str | None = Field(
        default=None,
        min_length=2,
        max_length=150,
    )

    sustainability_score: float | None = Field(
        default=None,
        ge=0,
        le=100,
    )

    carbon_rating: float | None = Field(
        default=None,
        ge=0,
    )

    recyclable: bool | None = None


class ProductESGProfileResponse(ORMBaseModel):
    id: int
    product_code: str
    product_name: str
    sustainability_score: float | None = None
    carbon_rating: float | None = None
    recyclable: bool
    created_at: datetime | None = None
    updated_at: datetime | None = None
