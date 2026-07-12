from pydantic import Field

from app.schemas.base import ORMBaseModel


class RewardCreate(ORMBaseModel):
    name: str = Field(
        min_length=2,
        max_length=100,
    )

    description: str | None = None

    points_required: int = Field(
        gt=0,
    )

    stock: int = Field(
        default=0,
        ge=0,
    )

    status: bool = True


class RewardUpdate(ORMBaseModel):
    name: str | None = Field(
        default=None,
        min_length=2,
        max_length=100,
    )

    description: str | None = None

    points_required: int | None = Field(
        default=None,
        gt=0,
    )

    stock: int | None = Field(
        default=None,
        ge=0,
    )

    status: bool | None = None


class RewardResponse(ORMBaseModel):
    id: int
    name: str
    description: str | None = None
    points_required: int
    stock: int
    status: bool
