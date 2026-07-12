from datetime import date
from typing import Literal

from pydantic import Field, model_validator

from app.schemas.base import ORMBaseModel


ComplianceSeverity = Literal[
    "Low",
    "Medium",
    "High",
    "Critical",
]

ComplianceStatus = Literal[
    "Open",
    "Pending",
    "In Progress",
    "Resolved",
    "Closed",
]


class ComplianceIssueCreate(ORMBaseModel):
    audit_id: int = Field(gt=0)

    severity: ComplianceSeverity

    description: str = Field(
        min_length=2,
    )

    owner: str = Field(
        min_length=2,
        max_length=100,
    )

    due_date: date

    status: ComplianceStatus = "Open"

    @model_validator(mode="after")
    def validate_owner_and_due_date(self):
        if not self.owner.strip():
            raise ValueError(
                "Compliance issue owner is required."
            )

        return self


class ComplianceIssueUpdate(ORMBaseModel):
    audit_id: int | None = Field(
        default=None,
        gt=0,
    )

    severity: ComplianceSeverity | None = None

    description: str | None = Field(
        default=None,
        min_length=2,
    )

    owner: str | None = Field(
        default=None,
        min_length=2,
        max_length=100,
    )

    due_date: date | None = None

    status: ComplianceStatus | None = None


class ComplianceIssueResponse(ORMBaseModel):
    id: int
    audit_id: int | None = None
    severity: str | None = None
    description: str | None = None
    owner: str | None = None
    due_date: date | None = None
    status: str | None = None
