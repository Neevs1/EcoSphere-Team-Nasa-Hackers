"""
Sprint 4 — Social (CSR Participation)
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
from app.models.csr_activity import CSRActivity
from app.models.employee_participation import (
    EmployeeParticipation,
)
from app.models.notification import Notification
from app.models.user import User


social_router = APIRouter(
    tags=["Social"],
)


# --- Schemas ---

class CSRActivityIn(BaseModel):
    title: str
    category_id: int | None = None
    description: str | None = None
    points: int = 0
    evidence_required: bool = False
    status: str = "Draft"
    start_date: date | None = None
    end_date: date | None = None


class CSRActivityOut(BaseModel):
    id: int
    title: str
    category_id: int | None = None
    description: str | None = None
    points: int
    evidence_required: bool
    status: str
    start_date: date | None = None
    end_date: date | None = None
    model_config = {"from_attributes": True}


class ParticipationOut(BaseModel):
    id: int
    employee_id: int
    activity_id: int
    proof_url: str | None = None
    approval_status: str
    points_earned: int
    completion_date: date | None = None
    model_config = {"from_attributes": True}


class DecisionIn(BaseModel):
    decision: str  # "Approved" | "Rejected"


class SocialDashboard(BaseModel):
    total_activities: int
    total_participations: int
    pending_approvals: int
    total_points_awarded: int


# --- Endpoints ---

@social_router.post(
    "/csr-activities",
    response_model=CSRActivityOut,
    status_code=status.HTTP_201_CREATED,
    summary="Create CSR activity",
)
def create_csr_activity(
    payload: CSRActivityIn,
    db: Session = Depends(get_db),
    current_user: User = Depends(
        require_role([
            "department_head",
            "esg_admin",
            "system_admin",
        ])
    ),
):
    activity = CSRActivity(
        **payload.model_dump()
    )
    db.add(activity)
    db.commit()
    db.refresh(activity)
    return activity


@social_router.get(
    "/csr-activities",
    response_model=list[CSRActivityOut],
    summary="List CSR activities",
)
def list_csr_activities(
    status_filter: str | None = Query(
        None, alias="status"
    ),
    category_id: int | None = None,
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=500),
    db: Session = Depends(get_db),
):
    stmt = select(CSRActivity)
    if status_filter:
        stmt = stmt.where(
            CSRActivity.status == status_filter
        )
    if category_id:
        stmt = stmt.where(
            CSRActivity.category_id == category_id
        )
    stmt = stmt.offset(skip).limit(limit)
    return list(db.scalars(stmt).all())


@social_router.post(
    "/csr-activities/{activity_id}/join",
    response_model=ParticipationOut,
    status_code=status.HTTP_201_CREATED,
    summary="Join a CSR activity",
)
def join_csr_activity(
    activity_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(
        get_current_user
    ),
):
    activity = db.get(CSRActivity, activity_id)
    if activity is None:
        raise HTTPException(
            404, "Activity not found."
        )
    if activity.status != "Open":
        raise HTTPException(
            409, "Activity is not open for joining."
        )

    existing = db.scalars(
        select(EmployeeParticipation).where(
            EmployeeParticipation.employee_id
            == current_user.id,
            EmployeeParticipation.activity_id
            == activity_id,
        )
    ).first()

    if existing:
        raise HTTPException(
            409,
            "Already joined this activity.",
        )

    participation = EmployeeParticipation(
        employee_id=current_user.id,
        activity_id=activity_id,
        approval_status="Pending",
    )
    db.add(participation)
    db.commit()
    db.refresh(participation)
    return participation


@social_router.patch(
    "/participations/{participation_id}/decision",
    response_model=ParticipationOut,
    summary="Approve or reject participation",
)
def decide_participation(
    participation_id: int,
    payload: DecisionIn,
    db: Session = Depends(get_db),
    current_user: User = Depends(
        require_role([
            "department_head",
            "esg_admin",
            "system_admin",
        ])
    ),
):
    participation = db.get(
        EmployeeParticipation,
        participation_id,
    )
    if participation is None:
        raise HTTPException(
            404, "Participation not found."
        )

    if payload.decision not in (
        "Approved",
        "Rejected",
    ):
        raise HTTPException(
            422,
            "Decision must be Approved or Rejected.",
        )

    activity = db.get(
        CSRActivity,
        participation.activity_id,
    )

    # Evidence check
    if (
        activity
        and activity.evidence_required
        and not participation.proof_url
        and payload.decision == "Approved"
    ):
        raise HTTPException(
            422,
            "Evidence required before approval.",
        )

    # Dept head scope check
    if current_user.role == "department_head":
        employee = db.get(
            User, participation.employee_id
        )
        if (
            employee
            and employee.department_id
            != current_user.department_id
        ):
            raise HTTPException(
                403,
                "Cannot approve outside your "
                "department.",
            )

    participation.approval_status = (
        payload.decision
    )

    if payload.decision == "Approved" and activity:
        participation.points_earned = (
            activity.points
        )
        participation.completion_date = (
            date.today()
        )

        # Credit points to employee
        employee = db.get(
            User, participation.employee_id
        )
        if employee:
            employee.points_balance += (
                activity.points
            )

        # Notification
        notif = Notification(
            recipient_id=participation.employee_id,
            type="csr_decision",
            message=(
                f"Your participation in "
                f"'{activity.title}' was approved. "
                f"+{activity.points} points!"
            ),
            priority="Informational",
            related_entity_type="participation",
            related_entity_id=participation.id,
        )
        db.add(notif)

    elif payload.decision == "Rejected":
        notif = Notification(
            recipient_id=participation.employee_id,
            type="csr_decision",
            message=(
                f"Your participation in "
                f"'{activity.title if activity else ''}' "
                f"was rejected."
            ),
            priority="Informational",
            related_entity_type="participation",
            related_entity_id=participation.id,
        )
        db.add(notif)

    db.commit()
    db.refresh(participation)
    return participation


@social_router.get(
    "/participations",
    response_model=list[ParticipationOut],
    summary="List participations (approval queue)",
)
def list_participations(
    status_filter: str | None = Query(
        None, alias="status"
    ),
    department_id: int | None = None,
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=500),
    db: Session = Depends(get_db),
):
    stmt = select(EmployeeParticipation)
    if status_filter:
        stmt = stmt.where(
            EmployeeParticipation.approval_status
            == status_filter
        )
    stmt = stmt.offset(skip).limit(limit)
    return list(db.scalars(stmt).all())


@social_router.get(
    "/social/dashboard",
    response_model=SocialDashboard,
    summary="Social dashboard",
)
def social_dashboard(
    db: Session = Depends(get_db),
):
    total_activities = (
        db.scalar(
            select(
                sa_func.count(CSRActivity.id)
            )
        )
        or 0
    )
    total_participations = (
        db.scalar(
            select(
                sa_func.count(
                    EmployeeParticipation.id
                )
            )
        )
        or 0
    )
    pending = (
        db.scalar(
            select(
                sa_func.count(
                    EmployeeParticipation.id
                )
            ).where(
                EmployeeParticipation.approval_status
                == "Pending"
            )
        )
        or 0
    )
    total_points = (
        db.scalar(
            select(
                sa_func.coalesce(
                    sa_func.sum(
                        EmployeeParticipation.points_earned
                    ),
                    0,
                )
            )
        )
        or 0
    )
    return SocialDashboard(
        total_activities=total_activities,
        total_participations=total_participations,
        pending_approvals=pending,
        total_points_awarded=total_points,
    )
