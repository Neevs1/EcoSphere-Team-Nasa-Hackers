from typing import Literal

from pydantic import Field

from app.schemas.base import ORMBaseModel


ChallengeApproval = Literal[
    "Pending",
    "Approved",
    "Rejected",
]


class ChallengeParticipationCreate(ORMBaseModel):
    challenge_id: int = Field(gt=0)

    employee_name: str = Field(
        min_length=2,
        max_length=100,
    )

    progress: int = Field(
        default=0,
        ge=0,
        le=100,
    )

    proof: str | None = Field(
        default=None,
        max_length=255,
    )

    approval: ChallengeApproval = "Pending"

    xp_awarded: int = Field(
        default=0,
        ge=0,
    )


class ChallengeParticipationUpdate(ORMBaseModel):
    challenge_id: int | None = Field(
        default=None,
        gt=0,
    )

    employee_name: str | None = Field(
        default=None,
        min_length=2,
        max_length=100,
    )

    progress: int | None = Field(
        default=None,
        ge=0,
        le=100,
    )

    proof: str | None = Field(
        default=None,
        max_length=255,
    )

    approval: ChallengeApproval | None = None

    xp_awarded: int | None = Field(
        default=None,
        ge=0,
    )


class ChallengeParticipationResponse(ORMBaseModel):
    id: int
    challenge_id: int | None = None
    employee_name: str | None = None
    progress: int | None = None
    proof: str | None = None
    approval: str | None = None
    xp_awarded: int | None = None
