from datetime import date
from typing import Literal

from pydantic import Field

from app.schemas.base import ORMBaseModel


AcknowledgementStatus = Literal[
    "Pending",
    "Acknowledged",
    "Declined",
]


class PolicyAcknowledgementCreate(ORMBaseModel):
    employee_name: str = Field(
        min_length=2,
        max_length=100,
    )

    policy_id: int = Field(gt=0)

    acknowledgement_date: date | None = None

    status: AcknowledgementStatus = "Pending"


class PolicyAcknowledgementUpdate(ORMBaseModel):
    employee_name: str | None = Field(
        default=None,
        min_length=2,
        max_length=100,
    )

    policy_id: int | None = Field(
        default=None,
        gt=0,
    )

    acknowledgement_date: date | None = None

    status: AcknowledgementStatus | None = None


class PolicyAcknowledgementResponse(ORMBaseModel):
    id: int
    employee_name: str | None = None
    policy_id: int | None = None
    acknowledgement_date: date | None = None
    status: str | None = None
