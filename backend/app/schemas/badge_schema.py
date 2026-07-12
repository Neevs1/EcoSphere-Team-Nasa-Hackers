from pydantic import Field

from app.schemas.base import ORMBaseModel


class BadgeCreate(ORMBaseModel):
    name: str = Field(
        min_length=2,
        max_length=100,
    )

    description: str | None = None

    unlock_rule: str | None = None

    icon: str | None = Field(
        default=None,
        max_length=255,
    )


class BadgeUpdate(ORMBaseModel):
    name: str | None = Field(
        default=None,
        min_length=2,
        max_length=100,
    )

    description: str | None = None

    unlock_rule: str | None = None

    icon: str | None = Field(
        default=None,
        max_length=255,
    )


class BadgeResponse(ORMBaseModel):
    id: int
    name: str
    description: str | None = None
    unlock_rule: str | None = None
    icon: str | None = None
