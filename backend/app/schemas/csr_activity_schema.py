from datetime import date

from pydantic import Field

from app.schemas.base import ORMBaseModel


class CSRActivityCreate(ORMBaseModel):
    title: str = Field(
        min_length=2,
        max_length=200,
    )

    category_id: int = Field(gt=0)

    description: str | None = None

    organizer: str | None = Field(
        default=None,
        max_length=100,
    )

    activity_date: date | None = None

    status: bool = True


class CSRActivityUpdate(ORMBaseModel):
    title: str | None = Field(
        default=None,
        min_length=2,
        max_length=200,
    )

    category_id: int | None = Field(
        default=None,
        gt=0,
    )

    description: str | None = None

    organizer: str | None = Field(
        default=None,
        max_length=100,
    )

    activity_date: date | None = None

    status: bool | None = None


class CSRActivityResponse(ORMBaseModel):
    id: int
    title: str
    category_id: int | None = None
    description: str | None = None
    organizer: str | None = None
    activity_date: date | None = None
    status: bool
