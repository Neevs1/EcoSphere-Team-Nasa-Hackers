from datetime import date
from typing import Literal

from pydantic import Field

from app.schemas.base import ORMBaseModel


AuditStatus = Literal[
    "Planned",
    "In Progress",
    "Completed",
    "Cancelled",
]


class AuditCreate(ORMBaseModel):
    department_id: int = Field(gt=0)

    audit_name: str = Field(
        min_length=2,
        max_length=150,
    )

    auditor: str | None = Field(
        default=None,
        max_length=100,
    )

    audit_date: date | None = None

    remarks: str | None = None

    status: AuditStatus = "Planned"


class AuditUpdate(ORMBaseModel):
    department_id: int | None = Field(
        default=None,
        gt=0,
    )

    audit_name: str | None = Field(
        default=None,
        min_length=2,
        max_length=150,
    )

    auditor: str | None = Field(
        default=None,
        max_length=100,
    )

    audit_date: date | None = None

    remarks: str | None = None

    status: AuditStatus | None = None


class AuditResponse(ORMBaseModel):
    id: int
    department_id: int | None = None
    audit_name: str | None = None
    auditor: str | None = None
    audit_date: date | None = None
    remarks: str | None = None
    status: str | None = None
