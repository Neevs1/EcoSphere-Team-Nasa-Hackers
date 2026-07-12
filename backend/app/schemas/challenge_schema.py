from datetime import date
from typing import Literal

from pydantic import Field, model_validator

from app.schemas.base import ORMBaseModel


ChallengeDifficulty = Literal[
    "Easy",
    "Medium",
    "Hard",
]

ChallengeStatus = Literal[
    "Draft",
    "Active",
    "Under Review",
    "Completed",
    "Archived",
]


class ChallengeCreate(ORMBaseModel):
    title: str = Field(
        min_length=2,
        max_length=200,
    )

    category_id: int = Field(gt=0)

    description: str | None = None

    xp: int = Field(
        default=0,
        ge=0,
    )

    difficulty: ChallengeDifficulty

    evidence_required: bool = False

    deadline: date | None = None

    status: ChallengeStatus = "Draft"

    @model_validator(mode="after")
    def validate_challenge(self):
        if (
            self.status in {"Active", "Under Review"}
            and self.deadline is None
        ):
            raise ValueError(
                "An active or under-review challenge requires a deadline."
            )

        return self


class ChallengeUpdate(ORMBaseModel):
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

    xp: int | None = Field(
        default=None,
        ge=0,
    )

    difficulty: ChallengeDifficulty | None = None

    evidence_required: bool | None = None

    deadline: date | None = None

    status: ChallengeStatus | None = None


class ChallengeResponse(ORMBaseModel):
    id: int
    title: str
    category_id: int | None = None
    description: str | None = None
    xp: int | None = None
    difficulty: str | None = None
    evidence_required: bool | None = None
    deadline: date | None = None
    status: str | None = None
