from datetime import date

from pydantic import Field

from app.schemas.base import ORMBaseModel


class ESGPolicyCreate(ORMBaseModel):
    title: str = Field(
        min_length=2,
        max_length=200,
    )

    description: str | None = None

    version: str | None = Field(
        default=None,
        max_length=20,
    )

    effective_date: date | None = None

    status: bool = True


class ESGPolicyUpdate(ORMBaseModel):
    title: str | None = Field(
        default=None,
        min_length=2,
        max_length=200,
    )

    description: str | None = None

    version: str | None = Field(
        default=None,
        max_length=20,
    )

    effective_date: date | None = None

    status: bool | None = None


class ESGPolicyResponse(ORMBaseModel):
    id: int
    title: str
    description: str | None = None
    version: str | None = None
    effective_date: date | None = None
    status: bool
