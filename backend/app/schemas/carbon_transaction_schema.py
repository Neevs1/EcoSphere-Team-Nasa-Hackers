from datetime import date, datetime

from pydantic import Field

from app.schemas.base import ORMBaseModel


class CarbonTransactionCreate(ORMBaseModel):
    department_id: int = Field(gt=0)

    emission_factor_id: int = Field(gt=0)

    product_profile_id: int | None = Field(
        default=None,
        gt=0,
    )

    activity: str = Field(
        min_length=2,
        max_length=150,
    )

    quantity: float = Field(gt=0)

    emission: float | None = Field(
        default=None,
        ge=0,
    )

    transaction_date: date


class CarbonTransactionUpdate(ORMBaseModel):
    department_id: int | None = Field(
        default=None,
        gt=0,
    )

    emission_factor_id: int | None = Field(
        default=None,
        gt=0,
    )

    product_profile_id: int | None = Field(
        default=None,
        gt=0,
    )

    activity: str | None = Field(
        default=None,
        min_length=2,
        max_length=150,
    )

    quantity: float | None = Field(
        default=None,
        gt=0,
    )

    emission: float | None = Field(
        default=None,
        ge=0,
    )

    transaction_date: date | None = None


class CarbonTransactionResponse(ORMBaseModel):
    id: int
    department_id: int
    emission_factor_id: int
    product_profile_id: int | None = None
    activity: str
    quantity: float
    emission: float
    transaction_date: date
    created_at: datetime | None = None
