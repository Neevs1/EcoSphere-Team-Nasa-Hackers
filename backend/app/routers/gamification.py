"""
Sprint 6 — Gamification (Challenges, Badges, Rewards)
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
from sqlalchemy import (
    select,
    update as sa_update,
    func as sa_func,
)
from sqlalchemy.orm import Session

from app.auth.dependencies import (
    get_current_user,
    require_role,
)
from app.database.db import get_db
from app.models.badge import Badge
from app.models.challenge import Challenge
from app.models.challenge_participation import (
    ChallengeParticipation,
)
from app.models.employee_badge import EmployeeBadge
from app.models.notification import Notification
from app.models.reward import Reward
from app.models.reward_redemption import (
    RewardRedemption,
)
from app.models.user import User


gamification_router = APIRouter(
    tags=["Gamification"],
)

# State machine transitions
VALID_TRANSITIONS = {
    "Draft": {"Active", "Archived"},
    "Active": {"Under Review", "Archived"},
    "Under Review": {"Completed", "Archived"},
}


# --- Schemas ---

class ChallengeIn(BaseModel):
    title: str
    category_id: int | None = None
    description: str | None = None
    xp: int = 0
    difficulty: str | None = None
    evidence_required: bool = False
    deadline: date | None = None
    status: str = "Draft"


class ChallengeOut(BaseModel):
    id: int
    title: str
    category_id: int | None = None
    description: str | None = None
    xp: int | None = None
    difficulty: str | None = None
    evidence_required: bool | None = None
    deadline: date | None = None
    status: str | None = None
    model_config = {"from_attributes": True}


class TransitionIn(BaseModel):
    target_status: str


class ChallengeParticipationOut(BaseModel):
    id: int
    challenge_id: int | None = None
    employee_id: int | None = None
    progress: int
    proof_url: str | None = None
    approval_status: str
    xp_awarded: int
    model_config = {"from_attributes": True}


class ChallengeDecisionIn(BaseModel):
    decision: str


class BadgeOut(BaseModel):
    id: int
    name: str
    description: str | None = None
    unlock_rule: dict | None = None
    icon_url: str | None = None
    status: bool | None = None
    model_config = {"from_attributes": True}


class EmployeeBadgeOut(BaseModel):
    id: int
    badge: BadgeOut
    awarded_at: str | None = None
    model_config = {"from_attributes": True}


class RewardOut(BaseModel):
    id: int
    name: str
    description: str | None = None
    points_required: int
    stock: int
    status: bool | None = None
    model_config = {"from_attributes": True}


class RedemptionOut(BaseModel):
    id: int
    employee_id: int
    reward_id: int
    points_deducted: int
    model_config = {"from_attributes": True}


class LeaderboardEntry(BaseModel):
    user_id: int
    name: str
    xp_total: int
    points_balance: int
    department_id: int | None = None


# --- Badge auto-award ---

def check_and_award_badges(
    db: Session, user: User
):
    badges = db.scalars(
        select(Badge).where(
            Badge.status.is_(True)
        )
    ).all()

    for badge in badges:
        rule = badge.unlock_rule
        if not rule or not isinstance(rule, dict):
            continue

        metric = rule.get("metric")
        threshold = rule.get("threshold", 0)

        qualified = False
        if metric == "xp" and user.xp_total >= threshold:
            qualified = True
        elif metric == "points" and user.points_balance >= threshold:
            qualified = True

        if not qualified:
            continue

        existing = db.scalars(
            select(EmployeeBadge).where(
                EmployeeBadge.employee_id == user.id,
                EmployeeBadge.badge_id == badge.id,
            )
        ).first()

        if existing:
            continue

        eb = EmployeeBadge(
            employee_id=user.id,
            badge_id=badge.id,
        )
        db.add(eb)

        notif = Notification(
            recipient_id=user.id,
            type="badge_unlocked",
            message=(
                f"🏆 Badge unlocked: {badge.name}!"
            ),
            priority="Informational",
            related_entity_type="badge",
            related_entity_id=badge.id,
        )
        db.add(notif)


# --- Endpoints ---

@gamification_router.post(
    "/challenges",
    response_model=ChallengeOut,
    status_code=status.HTTP_201_CREATED,
    summary="Create challenge",
)
def create_challenge(
    payload: ChallengeIn,
    db: Session = Depends(get_db),
    current_user: User = Depends(
        require_role([
            "esg_admin", "system_admin"
        ])
    ),
):
    challenge = Challenge(
        **payload.model_dump()
    )
    db.add(challenge)
    db.commit()
    db.refresh(challenge)
    return challenge


@gamification_router.get(
    "/challenges",
    response_model=list[ChallengeOut],
    summary="List challenges",
)
def list_challenges(
    status_filter: str | None = Query(
        None, alias="status"
    ),
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=500),
    db: Session = Depends(get_db),
):
    stmt = select(Challenge)
    if status_filter:
        stmt = stmt.where(
            Challenge.status == status_filter
        )
    stmt = stmt.offset(skip).limit(limit)
    return list(db.scalars(stmt).all())


@gamification_router.post(
    "/challenges/{challenge_id}/transition",
    response_model=ChallengeOut,
    summary="Transition challenge status",
)
def transition_challenge(
    challenge_id: int,
    payload: TransitionIn,
    db: Session = Depends(get_db),
    current_user: User = Depends(
        require_role([
            "esg_admin", "system_admin"
        ])
    ),
):
    challenge = db.get(Challenge, challenge_id)
    if challenge is None:
        raise HTTPException(
            404, "Challenge not found."
        )

    current = challenge.status
    target = payload.target_status

    allowed = VALID_TRANSITIONS.get(current, set())
    if target not in allowed:
        raise HTTPException(
            409,
            f"Cannot transition from "
            f"'{current}' to '{target}'.",
        )

    # Under Review → Completed requires no
    # pending participations
    if (
        current == "Under Review"
        and target == "Completed"
    ):
        pending = db.scalar(
            select(
                sa_func.count(
                    ChallengeParticipation.id
                )
            ).where(
                ChallengeParticipation.challenge_id
                == challenge_id,
                ChallengeParticipation.approval_status
                == "Pending",
            )
        )
        if pending and pending > 0:
            raise HTTPException(
                409,
                "Cannot complete — there are "
                f"{pending} pending participations.",
            )

    challenge.status = target
    db.commit()
    db.refresh(challenge)
    return challenge


@gamification_router.post(
    "/challenges/{challenge_id}/join",
    response_model=ChallengeParticipationOut,
    status_code=status.HTTP_201_CREATED,
    summary="Join a challenge",
)
def join_challenge(
    challenge_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(
        get_current_user
    ),
):
    challenge = db.get(Challenge, challenge_id)
    if challenge is None:
        raise HTTPException(
            404, "Challenge not found."
        )
    if challenge.status != "Active":
        raise HTTPException(
            409, "Challenge is not active."
        )

    existing = db.scalars(
        select(ChallengeParticipation).where(
            ChallengeParticipation.challenge_id
            == challenge_id,
            ChallengeParticipation.employee_id
            == current_user.id,
        )
    ).first()

    if existing:
        raise HTTPException(
            409, "Already joined this challenge."
        )

    cp = ChallengeParticipation(
        challenge_id=challenge_id,
        employee_id=current_user.id,
        progress=0,
        approval_status="Pending",
        xp_awarded=0,
    )
    db.add(cp)
    db.commit()
    db.refresh(cp)
    return cp


@gamification_router.patch(
    "/challenge-participations/{cp_id}/decision",
    response_model=ChallengeParticipationOut,
    summary="Approve or reject challenge participation",
)
def decide_challenge_participation(
    cp_id: int,
    payload: ChallengeDecisionIn,
    db: Session = Depends(get_db),
    current_user: User = Depends(
        require_role([
            "esg_admin", "system_admin"
        ])
    ),
):
    cp = db.get(ChallengeParticipation, cp_id)
    if cp is None:
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

    cp.approval_status = payload.decision

    if payload.decision == "Approved":
        challenge = db.get(
            Challenge, cp.challenge_id
        )
        xp = challenge.xp if challenge else 0
        cp.xp_awarded = xp
        cp.progress = 100

        employee = db.get(User, cp.employee_id)
        if employee:
            employee.xp_total += xp
            check_and_award_badges(db, employee)

        notif = Notification(
            recipient_id=cp.employee_id,
            type="challenge_decision",
            message=(
                f"Your challenge participation was "
                f"approved! +{xp} XP"
            ),
            priority="Informational",
            related_entity_type="challenge_participation",
            related_entity_id=cp.id,
        )
        db.add(notif)
    else:
        notif = Notification(
            recipient_id=cp.employee_id,
            type="challenge_decision",
            message=(
                "Your challenge participation "
                "was rejected."
            ),
            priority="Informational",
            related_entity_type="challenge_participation",
            related_entity_id=cp.id,
        )
        db.add(notif)

    db.commit()
    db.refresh(cp)
    return cp


@gamification_router.get(
    "/badges",
    response_model=list[BadgeOut],
    summary="List all badges",
)
def list_badges(
    db: Session = Depends(get_db),
):
    return list(
        db.scalars(select(Badge)).all()
    )


@gamification_router.get(
    "/employees/{employee_id}/badges",
    response_model=list[BadgeOut],
    summary="List employee's badges",
)
def list_employee_badges(
    employee_id: int,
    db: Session = Depends(get_db),
):
    ebs = db.scalars(
        select(EmployeeBadge).where(
            EmployeeBadge.employee_id
            == employee_id
        )
    ).all()

    badges = []
    for eb in ebs:
        badge = db.get(Badge, eb.badge_id)
        if badge:
            badges.append(badge)
    return badges


@gamification_router.post(
    "/rewards/{reward_id}/redeem",
    response_model=RedemptionOut,
    status_code=status.HTTP_201_CREATED,
    summary="Redeem a reward (atomic)",
)
def redeem_reward(
    reward_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(
        get_current_user
    ),
):
    # Atomic: conditional UPDATE
    result = db.execute(
        sa_update(Reward)
        .where(
            Reward.id == reward_id,
            Reward.stock > 0,
            Reward.status.is_(True),
        )
        .values(stock=Reward.stock - 1)
    )

    if result.rowcount == 0:
        raise HTTPException(
            409,
            "Reward out of stock or inactive.",
        )

    reward = db.get(Reward, reward_id)

    if (
        current_user.points_balance
        < reward.points_required
    ):
        db.rollback()
        raise HTTPException(
            409,
            "Insufficient points.",
        )

    current_user.points_balance -= (
        reward.points_required
    )

    redemption = RewardRedemption(
        employee_id=current_user.id,
        reward_id=reward_id,
        points_deducted=reward.points_required,
    )
    db.add(redemption)
    db.commit()
    db.refresh(redemption)
    return redemption


@gamification_router.get(
    "/gamification/leaderboard",
    response_model=list[LeaderboardEntry],
    summary="XP leaderboard",
)
def leaderboard(
    department_id: int | None = None,
    limit: int = Query(20, ge=1, le=100),
    db: Session = Depends(get_db),
):
    stmt = select(User).where(
        User.role == "employee"
    )
    if department_id:
        stmt = stmt.where(
            User.department_id == department_id
        )
    stmt = stmt.order_by(
        User.xp_total.desc()
    ).limit(limit)

    users = db.scalars(stmt).all()

    return [
        LeaderboardEntry(
            user_id=u.id,
            name=u.name,
            xp_total=u.xp_total,
            points_balance=u.points_balance,
            department_id=u.department_id,
        )
        for u in users
    ]
