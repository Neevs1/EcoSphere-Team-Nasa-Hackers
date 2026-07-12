"""
Sprint 7 — Scoring Engine, Dashboard & Reports
"""
from datetime import date, datetime, timezone

from fastapi import (
    APIRouter,
    Depends,
    Query,
)
from pydantic import BaseModel
from sqlalchemy import select, func as sa_func
from sqlalchemy.orm import Session

from app.database.db import get_db
from app.models.carbon_transaction import (
    CarbonTransaction,
)
from app.models.compliance_issue import (
    ComplianceIssue,
)
from app.models.department import Department
from app.models.department_score import (
    DepartmentScore,
)
from app.models.employee_participation import (
    EmployeeParticipation,
)
from app.models.environmental_goal import (
    EnvironmentalGoal,
)
from app.models.esg_configuration import (
    EsgConfiguration,
)
from app.models.user import User


dashboard_router = APIRouter(
    tags=["Dashboard & Reports"],
)

SEVERITY_WEIGHTS = {
    "Critical": 4,
    "High": 3,
    "Medium": 2,
    "Low": 1,
}


def compute_environmental_score(
    db: Session, department_id: int
) -> float:
    goals = db.scalars(
        select(EnvironmentalGoal).where(
            EnvironmentalGoal.department_id
            == department_id,
            EnvironmentalGoal.status.is_(True),
        )
    ).all()

    if not goals:
        return 100.0

    ratios = []
    for g in goals:
        target = g.target_co2 or 1
        current = g.current_co2 or 0
        ratio = min(100, (current / target) * 100)
        ratios.append(ratio)

    avg_ratio = sum(ratios) / len(ratios)
    return round(max(0, 100 - avg_ratio), 2)


def compute_social_score(
    db: Session, department_id: int
) -> float:
    total_employees = db.scalar(
        select(sa_func.count(User.id)).where(
            User.department_id == department_id,
        )
    ) or 1

    approved = db.scalar(
        select(
            sa_func.count(
                EmployeeParticipation.id
            )
        )
        .join(
            User,
            EmployeeParticipation.employee_id
            == User.id,
        )
        .where(
            User.department_id == department_id,
            EmployeeParticipation.approval_status
            == "Approved",
        )
    ) or 0

    return round(
        min(
            100,
            (approved / total_employees) * 100,
        ),
        2,
    )


def compute_governance_score(
    db: Session, department_id: int
) -> float:
    issues = db.scalars(
        select(ComplianceIssue).where(
            ComplianceIssue.department_id
            == department_id,
            ComplianceIssue.status == "Open",
        )
    ).all()

    weighted_sum = sum(
        SEVERITY_WEIGHTS.get(i.severity, 1)
        for i in issues
    )

    return round(
        max(0, 100 - min(100, weighted_sum * 5)),
        2,
    )


# --- Schemas ---

class ScoreOut(BaseModel):
    department_id: int
    department_name: str
    environmental: float
    social: float
    governance: float
    overall: float


class DashboardOut(BaseModel):
    scores: list[ScoreOut]
    overall_score: float


class ReportRow(BaseModel):
    label: str
    value: float
    detail: str | None = None


# --- Endpoints ---

@dashboard_router.get(
    "/dashboard/scores",
    response_model=DashboardOut,
    summary="Get ESG dashboard scores",
)
def get_dashboard_scores(
    department_id: int | None = None,
    db: Session = Depends(get_db),
):
    config = db.get(EsgConfiguration, 1)
    env_w = config.environmental_weight if config else 0.4
    soc_w = config.social_weight if config else 0.3
    gov_w = config.governance_weight if config else 0.3

    dept_query = select(Department).where(
        Department.status.is_(True)
    )
    if department_id:
        dept_query = dept_query.where(
            Department.id == department_id
        )

    departments = db.scalars(dept_query).all()
    scores = []

    for dept in departments:
        env = compute_environmental_score(
            db, dept.id
        )
        soc = compute_social_score(db, dept.id)
        gov = compute_governance_score(
            db, dept.id
        )
        overall = round(
            env * env_w + soc * soc_w + gov * gov_w,
            2,
        )

        # Cache score
        ds = DepartmentScore(
            department_id=dept.id,
            period=date.today().strftime("%Y-%m"),
            environmental_score=env,
            social_score=soc,
            governance_score=gov,
            total_score=overall,
        )
        db.add(ds)

        scores.append(
            ScoreOut(
                department_id=dept.id,
                department_name=dept.name,
                environmental=env,
                social=soc,
                governance=gov,
                overall=overall,
            )
        )

    db.commit()

    org_overall = (
        round(
            sum(s.overall for s in scores)
            / len(scores),
            2,
        )
        if scores
        else 0
    )

    return DashboardOut(
        scores=scores,
        overall_score=org_overall,
    )


@dashboard_router.get(
    "/reports/{report_type}",
    response_model=list[ReportRow],
    summary="Get canned report",
)
def get_report(
    report_type: str,
    department_id: int | None = None,
    date_from: date | None = None,
    date_to: date | None = None,
    db: Session = Depends(get_db),
):
    if report_type == "environmental":
        stmt = select(CarbonTransaction)
        if department_id:
            stmt = stmt.where(
                CarbonTransaction.department_id
                == department_id
            )
        if date_from:
            stmt = stmt.where(
                CarbonTransaction.transaction_date
                >= date_from
            )
        if date_to:
            stmt = stmt.where(
                CarbonTransaction.transaction_date
                <= date_to
            )
        txns = db.scalars(stmt).all()
        return [
            ReportRow(
                label=f"Txn #{t.id}",
                value=t.co2_calculated,
                detail=str(t.transaction_date),
            )
            for t in txns
        ]

    elif report_type == "social":
        stmt = select(EmployeeParticipation)
        rows = db.scalars(stmt).all()
        return [
            ReportRow(
                label=f"Participation #{r.id}",
                value=float(r.points_earned or 0),
                detail=r.approval_status,
            )
            for r in rows
        ]

    elif report_type == "governance":
        stmt = select(ComplianceIssue)
        if department_id:
            stmt = stmt.where(
                ComplianceIssue.department_id
                == department_id
            )
        issues = db.scalars(stmt).all()
        return [
            ReportRow(
                label=f"Issue #{i.id}",
                value=float(
                    SEVERITY_WEIGHTS.get(
                        i.severity, 1
                    )
                ),
                detail=(
                    f"{i.severity} - {i.status}"
                ),
            )
            for i in issues
        ]

    elif report_type == "esg-summary":
        depts = db.scalars(
            select(Department).where(
                Department.status.is_(True)
            )
        ).all()

        config = db.get(EsgConfiguration, 1)
        env_w = config.environmental_weight if config else 0.4
        soc_w = config.social_weight if config else 0.3
        gov_w = config.governance_weight if config else 0.3

        return [
            ReportRow(
                label=dept.name,
                value=round(
                    compute_environmental_score(
                        db, dept.id
                    )
                    * env_w
                    + compute_social_score(
                        db, dept.id
                    )
                    * soc_w
                    + compute_governance_score(
                        db, dept.id
                    )
                    * gov_w,
                    2,
                ),
                detail=dept.code,
            )
            for dept in depts
        ]

    return []
