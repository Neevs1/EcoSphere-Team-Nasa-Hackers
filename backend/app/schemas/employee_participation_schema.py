from datetime import date
from typing import Literal

from pydantic import Field

from app.schemas.base import ORMBaseModel


ApprovalStatus = Literal[
    "Pending",
    "Approved",
    "Rejected",
]


class EmployeeParticipationCreate(ORMBaseModel):
    employee_name: str = Field(
        min_length=2,
        max_length=100,
    )

    csr_activity_id: int = Field(gt=0)

    proof: str | None = Field(
        default=None,
        max_length=255,
    )

    approval_status: ApprovalStatus = "Pending"

    points_earned: int = Field(
        default=0,
        ge=0,
    )

    completion_date: date | None = None


class EmployeeParticipationUpdate(ORMBaseModel):
    employee_name: str | None = Field(
        default=None,
        min_length=2,
        max_length=100,
    )

    csr_activity_id: int | None = Field(
        default=None,
        gt=0,
    )

    proof: str | None = Field(
        default=None,
        max_length=255,
    )

    approval_status: ApprovalStatus | None = None

    points_earned: int | None = Field(
        default=None,
        ge=0,
    )

    completion_date: date | None = None


class EmployeeParticipationResponse(ORMBaseModel):
    id: int
    employee_name: str
    csr_activity_id: int | None = None
    proof: str | None = None
    approval_status: str | None = None
    points_earned: int | None = None
    completion_date: date | None = None
