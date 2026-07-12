"""
Sprint 5 — Governance (Audits + Compliance Issues)
"""
from datetime import date

from fastapi import (
    APIRouter,
    Depends,
    HTTPException,
    Query,
    status,
)
from pydantic import BaseModel
from sqlalchemy import select, func as sa_func
from sqlalchemy.orm import Session

from app.auth.dependencies import (
    get_current_user,
    require_role,
)
from app.database.db import get_db
from app.models.audit import Audit
from app.models.compliance_issue import (
    ComplianceIssue,
)
from app.models.notification import Notification
from app.models.user import User


governance_router = APIRouter(
    tags=["Governance"],
)


# --- Schemas ---

class AuditIn(BaseModel):
    title: str
    department_id: int | None = None
    auditor_id: int | None = None
    audit_date: date | None = None
    findings_summary: str | None = None


class AuditOut(BaseModel):
    id: int
    title: str
    department_id: int | None = None
    auditor_id: int | None = None
    audit_date: date | None = None
    findings_summary: str | None = None
    status: str
    model_config = {"from_attributes": True}


class ComplianceIssueIn(BaseModel):
    audit_id: int | None = None
    severity: str
    description: str | None = None
    owner_id: int
    department_id: int | None = None
    due_date: date


class ComplianceIssueOut(BaseModel):
    id: int
    audit_id: int | None = None
    severity: str
    description: str | None = None
    owner_id: int
    department_id: int | None = None
    due_date: date
    status: str
    is_overdue: bool = False
    model_config = {"from_attributes": True}


# --- Endpoints ---

@governance_router.post(
    "/audits",
    response_model=AuditOut,
    status_code=status.HTTP_201_CREATED,
    summary="Create audit",
)
def create_audit(
    payload: AuditIn,
    db: Session = Depends(get_db),
    current_user: User = Depends(
        require_role([
            "compliance_officer",
            "system_admin",
        ])
    ),
):
    audit = Audit(**payload.model_dump())
    db.add(audit)
    db.commit()
    db.refresh(audit)
    return audit


@governance_router.get(
    "/audits",
    response_model=list[AuditOut],
    summary="List audits",
)
def list_audits(
    department_id: int | None = None,
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=500),
    db: Session = Depends(get_db),
):
    stmt = select(Audit)
    if department_id:
        stmt = stmt.where(
            Audit.department_id == department_id
        )
    stmt = stmt.offset(skip).limit(limit)
    return list(db.scalars(stmt).all())


@governance_router.post(
    "/compliance-issues",
    response_model=ComplianceIssueOut,
    status_code=status.HTTP_201_CREATED,
    summary="Create compliance issue",
)
def create_compliance_issue(
    payload: ComplianceIssueIn,
    db: Session = Depends(get_db),
    current_user: User = Depends(
        require_role([
            "compliance_officer",
            "esg_admin",
            "system_admin",
        ])
    ),
):
    if not payload.owner_id:
        raise HTTPException(
            422, "owner_id is required."
        )
    if not payload.due_date:
        raise HTTPException(
            422, "due_date is required."
        )

    issue = ComplianceIssue(
        **payload.model_dump()
    )
    db.add(issue)
    db.flush()

    # Notify owner
    notif = Notification(
        recipient_id=payload.owner_id,
        type="compliance_issue",
        message=(
            f"New compliance issue assigned to you: "
            f"{payload.severity} severity — "
            f"due {payload.due_date}."
        ),
        priority="Actionable",
        related_entity_type="compliance_issue",
        related_entity_id=issue.id,
    )
    db.add(notif)

    # Notify all compliance officers
    officers = db.scalars(
        select(User).where(
            User.role == "compliance_officer",
            User.id != payload.owner_id,
        )
    ).all()

    for officer in officers:
        db.add(
            Notification(
                recipient_id=officer.id,
                type="compliance_issue",
                message=(
                    f"New {payload.severity} "
                    f"compliance issue raised."
                ),
                priority="Informational",
                related_entity_type="compliance_issue",
                related_entity_id=issue.id,
            )
        )

    db.commit()
    db.refresh(issue)

    out = ComplianceIssueOut.model_validate(issue)
    out.is_overdue = (
        issue.status == "Open"
        and issue.due_date < date.today()
    )
    return out


@governance_router.patch(
    "/compliance-issues/{issue_id}/resolve",
    response_model=ComplianceIssueOut,
    summary="Resolve compliance issue",
)
def resolve_compliance_issue(
    issue_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(
        get_current_user
    ),
):
    issue = db.get(ComplianceIssue, issue_id)
    if issue is None:
        raise HTTPException(
            404, "Compliance issue not found."
        )

    if date.today() <= issue.due_date:
        issue.status = "Resolved"
    else:
        issue.status = "Resolved Late"

    db.commit()
    db.refresh(issue)

    out = ComplianceIssueOut.model_validate(issue)
    out.is_overdue = False
    return out


@governance_router.get(
    "/compliance-issues",
    response_model=list[ComplianceIssueOut],
    summary="List compliance issues",
)
def list_compliance_issues(
    status_filter: str | None = Query(
        None, alias="status"
    ),
    overdue: bool | None = None,
    department_id: int | None = None,
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=500),
    db: Session = Depends(get_db),
):
    stmt = select(ComplianceIssue)

    if status_filter:
        stmt = stmt.where(
            ComplianceIssue.status == status_filter
        )
    if department_id:
        stmt = stmt.where(
            ComplianceIssue.department_id
            == department_id
        )
    if overdue:
        stmt = stmt.where(
            ComplianceIssue.due_date
            < date.today(),
            ComplianceIssue.status == "Open",
        )

    stmt = stmt.offset(skip).limit(limit)
    issues = list(db.scalars(stmt).all())

    result = []
    for issue in issues:
        out = ComplianceIssueOut.model_validate(
            issue
        )
        out.is_overdue = (
            issue.status == "Open"
            and issue.due_date < date.today()
        )
        result.append(out)

    return result
