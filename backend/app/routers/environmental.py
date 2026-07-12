"""
Sprint 3 — Environmental (Carbon Transactions)
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
from app.models.carbon_transaction import (
    CarbonTransaction,
)
from app.models.department import Department
from app.models.emission_factor import EmissionFactor
from app.models.environmental_goal import (
    EnvironmentalGoal,
)
from app.models.esg_configuration import (
    EsgConfiguration,
)
from app.models.operational_record import (
    OperationalRecord,
)
from app.models.user import User


environmental_router = APIRouter(
    tags=["Environmental"],
)


# --- Schemas ---

class CarbonTransactionOut(BaseModel):
    id: int
    department_id: int
    source_type: str
    source_record_id: int | None = None
    emission_factor_id: int
    quantity: float
    co2_calculated: float
    transaction_date: date
    created_by: int | None = None
    model_config = {"from_attributes": True}


class CarbonTransactionIn(BaseModel):
    department_id: int
    emission_factor_id: int
    quantity: float
    transaction_date: date
    source_type: str = "Manual"


class OperationalRecordIn(BaseModel):
    department_id: int
    source_type: str
    quantity: float
    emission_factor_id: int


class OperationalRecordOut(BaseModel):
    id: int
    department_id: int
    source_type: str
    quantity: float
    emission_factor_id: int
    model_config = {"from_attributes": True}


class GoalOut(BaseModel):
    id: int
    department_id: int | None = None
    name: str
    target_co2: float | None = None
    current_co2: float | None = None
    deadline: date | None = None
    status: bool | None = None
    model_config = {"from_attributes": True}


class EnvironmentalDashboard(BaseModel):
    total_emissions: float
    total_transactions: int
    goals: list[GoalOut]
    recent_transactions: list[CarbonTransactionOut]


# --- Helpers ---

def _recalculate_goals(
    db: Session, department_id: int
):
    """
    Update current_co2 on all active goals
    for a department.
    """
    total = db.scalar(
        select(
            sa_func.coalesce(
                sa_func.sum(
                    CarbonTransaction.co2_calculated
                ),
                0.0,
            )
        ).where(
            CarbonTransaction.department_id
            == department_id
        )
    )

    goals = db.scalars(
        select(EnvironmentalGoal).where(
            EnvironmentalGoal.department_id
            == department_id,
            EnvironmentalGoal.status.is_(True),
        )
    ).all()

    for goal in goals:
        goal.current_co2 = total


# --- Endpoints ---

@environmental_router.post(
    "/operational-records",
    response_model=OperationalRecordOut,
    status_code=status.HTTP_201_CREATED,
    summary="Create operational record",
)
def create_operational_record(
    payload: OperationalRecordIn,
    db: Session = Depends(get_db),
    current_user: User = Depends(
        get_current_user
    ),
):
    ef = db.get(
        EmissionFactor,
        payload.emission_factor_id,
    )
    if ef is None or not ef.status:
        raise HTTPException(
            422,
            "Emission factor not found or inactive.",
        )

    record = OperationalRecord(
        **payload.model_dump()
    )
    db.add(record)
    db.flush()

    config = db.get(EsgConfiguration, 1)

    if config and config.auto_emission_calculation:
        co2 = round(
            payload.quantity * ef.factor, 4
        )
        txn = CarbonTransaction(
            department_id=payload.department_id,
            source_type=payload.source_type,
            source_record_id=record.id,
            emission_factor_id=payload.emission_factor_id,
            quantity=payload.quantity,
            co2_calculated=co2,
            transaction_date=date.today(),
            created_by=current_user.id,
        )
        db.add(txn)
        _recalculate_goals(
            db, payload.department_id
        )

    db.commit()
    db.refresh(record)
    return record


@environmental_router.post(
    "/carbon-transactions",
    response_model=CarbonTransactionOut,
    status_code=status.HTTP_201_CREATED,
    summary="Create manual carbon transaction",
)
def create_carbon_transaction(
    payload: CarbonTransactionIn,
    db: Session = Depends(get_db),
    current_user: User = Depends(
        get_current_user
    ),
):
    config = db.get(EsgConfiguration, 1)
    if config and config.auto_emission_calculation:
        raise HTTPException(
            status.HTTP_409_CONFLICT,
            "Manual entry blocked — auto emission "
            "calculation is enabled.",
        )

    if payload.quantity <= 0:
        raise HTTPException(
            422, "Quantity must be positive."
        )

    ef = db.get(
        EmissionFactor,
        payload.emission_factor_id,
    )
    if ef is None or not ef.status:
        raise HTTPException(
            422,
            "Emission factor not found or inactive.",
        )

    co2 = round(
        payload.quantity * ef.factor, 4
    )
    txn = CarbonTransaction(
        department_id=payload.department_id,
        source_type=payload.source_type,
        emission_factor_id=payload.emission_factor_id,
        quantity=payload.quantity,
        co2_calculated=co2,
        transaction_date=payload.transaction_date,
        created_by=current_user.id,
    )
    db.add(txn)
    _recalculate_goals(
        db, payload.department_id
    )
    db.commit()
    db.refresh(txn)
    return txn


@environmental_router.get(
    "/carbon-transactions",
    response_model=list[CarbonTransactionOut],
    summary="List carbon transactions",
)
def list_carbon_transactions(
    department_id: int | None = None,
    date_from: date | None = None,
    date_to: date | None = None,
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=500),
    db: Session = Depends(get_db),
):
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

    stmt = (
        stmt.order_by(
            CarbonTransaction.id.desc()
        )
        .offset(skip)
        .limit(limit)
    )

    return list(
        db.scalars(stmt).all()
    )


@environmental_router.post(
    "/carbon-transactions/{txn_id}/reverse",
    response_model=CarbonTransactionOut,
    status_code=status.HTTP_201_CREATED,
    summary="Reverse a carbon transaction",
)
def reverse_carbon_transaction(
    txn_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(
        get_current_user
    ),
):
    original = db.get(CarbonTransaction, txn_id)
    if original is None:
        raise HTTPException(
            404, "Transaction not found."
        )

    reversal = CarbonTransaction(
        department_id=original.department_id,
        source_type=original.source_type,
        source_record_id=original.source_record_id,
        emission_factor_id=original.emission_factor_id,
        quantity=-original.quantity,
        co2_calculated=-original.co2_calculated,
        transaction_date=date.today(),
        created_by=current_user.id,
    )
    db.add(reversal)
    _recalculate_goals(
        db, original.department_id
    )
    db.commit()
    db.refresh(reversal)
    return reversal


@environmental_router.get(
    "/environmental/dashboard",
    response_model=EnvironmentalDashboard,
    summary="Environmental dashboard",
)
def environmental_dashboard(
    department_id: int | None = None,
    db: Session = Depends(get_db),
):
    txn_query = select(CarbonTransaction)
    goal_query = select(EnvironmentalGoal)

    if department_id:
        txn_query = txn_query.where(
            CarbonTransaction.department_id
            == department_id
        )
        goal_query = goal_query.where(
            EnvironmentalGoal.department_id
            == department_id
        )

    txns = list(
        db.scalars(
            txn_query.order_by(
                CarbonTransaction.id.desc()
            ).limit(10)
        ).all()
    )

    total_emissions = db.scalar(
        select(
            sa_func.coalesce(
                sa_func.sum(
                    CarbonTransaction.co2_calculated
                ),
                0.0,
            )
        ).where(
            CarbonTransaction.department_id
            == department_id
            if department_id
            else True
        )
    )

    total_count = db.scalar(
        select(
            sa_func.count(CarbonTransaction.id)
        ).where(
            CarbonTransaction.department_id
            == department_id
            if department_id
            else True
        )
    )

    goals = list(
        db.scalars(goal_query).all()
    )

    return EnvironmentalDashboard(
        total_emissions=total_emissions or 0,
        total_transactions=total_count or 0,
        goals=[
            GoalOut.model_validate(g)
            for g in goals
        ],
        recent_transactions=[
            CarbonTransactionOut.model_validate(t)
            for t in txns
        ],
    )
