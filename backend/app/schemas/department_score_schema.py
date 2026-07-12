from pydantic import Field

from app.schemas.base import ORMBaseModel


class DepartmentScoreCreate(ORMBaseModel):
    department_id: int = Field(gt=0)

    environmental_score: float = Field(
        ge=0,
        le=100,
    )

    social_score: float = Field(
        ge=0,
        le=100,
    )

    governance_score: float = Field(
        ge=0,
        le=100,
    )

    total_score: float | None = Field(
        default=None,
        ge=0,
        le=100,
    )


class DepartmentScoreUpdate(ORMBaseModel):
    department_id: int | None = Field(
        default=None,
        gt=0,
    )

    environmental_score: float | None = Field(
        default=None,
        ge=0,
        le=100,
    )

    social_score: float | None = Field(
        default=None,
        ge=0,
        le=100,
    )

    governance_score: float | None = Field(
        default=None,
        ge=0,
        le=100,
    )

    total_score: float | None = Field(
        default=None,
        ge=0,
        le=100,
    )


class DepartmentScoreResponse(ORMBaseModel):
    id: int
    department_id: int | None = None
    environmental_score: float | None = None
    social_score: float | None = None
    governance_score: float | None = None
    total_score: float | None = None
