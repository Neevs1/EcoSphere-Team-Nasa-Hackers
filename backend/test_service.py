from datetime import date

from sqlalchemy import select
from sqlalchemy.exc import IntegrityError

from app.crud import (
    department_crud,
    emission_factor_crud,
)
from app.database.db import SessionLocal
from app.models import (
    CarbonTransaction,
    Department,
    DepartmentScore,
    EmissionFactor,
)
from app.schemas import (
    CarbonTransactionCreate,
    DepartmentCreate,
    DepartmentScoreCreate,
    EmissionFactorCreate,
)
from app.services import (
    carbon_service,
    department_esg_score_service,
    department_service,
)


def get_or_create_department(db):
    statement = select(Department).where(
        Department.code == "FIN"
    )

    existing_department = db.scalar(statement)

    if existing_department is not None:
        print(
            f"Using existing department: "
            f"{existing_department.id} - "
            f"{existing_department.name}"
        )
        return existing_department

    department = department_service.create(
        db,
        DepartmentCreate(
            name="Finance",
            code="FIN",
            head="Finance Manager",
            employee_count=12,
            status=True,
        ),
    )

    print(
        f"Department created: "
        f"{department.id} - {department.name}"
    )

    return department


def get_or_create_emission_factor(db):
    statement = select(EmissionFactor).where(
        EmissionFactor.source == "Grid Electricity",
        EmissionFactor.category == "Energy",
    )

    existing_factor = db.scalar(statement)

    if existing_factor is not None:
        print(
            f"Using existing emission factor: "
            f"{existing_factor.id} - "
            f"{existing_factor.factor}"
        )
        return existing_factor

    factor = emission_factor_crud.create(
        db,
        obj_in=EmissionFactorCreate(
            source="Grid Electricity",
            category="Energy",
            factor=0.82,
            unit="kg CO2e/kWh",
            status=True,
        ),
    )

    print(
        f"Emission factor created: "
        f"{factor.id} - {factor.factor}"
    )

    return factor


def test_generic_department_service(db):
    print("\n1. Testing generic Department service")

    department = get_or_create_department(db)

    fetched_department = department_service.get(
        db,
        department.id,
    )

    if fetched_department is None:
        raise RuntimeError(
            "Department could not be retrieved."
        )

    print("Department retrieved successfully")
    print("ID:", fetched_department.id)
    print("Name:", fetched_department.name)
    print("Code:", fetched_department.code)


def test_carbon_service(
    db,
    department,
    emission_factor,
):
    print("\n2. Testing automatic carbon calculation")

    transaction = carbon_service.create_transaction(
        db,
        CarbonTransactionCreate(
            department_id=department.id,
            emission_factor_id=emission_factor.id,
            product_profile_id=None,
            activity="Office electricity consumption",
            quantity=100,
            transaction_date=date.today(),
        ),
    )

    expected_emission = round(
        100 * emission_factor.factor,
        4,
    )

    print("Carbon transaction created")
    print("Transaction ID:", transaction.id)
    print("Quantity:", transaction.quantity)
    print("Calculated emission:", transaction.emission)
    print("Expected emission:", expected_emission)

    if transaction.emission != expected_emission:
        raise AssertionError(
            "Carbon emission calculation is incorrect."
        )


def test_esg_score_service(
    db,
    department,
):
    print("\n3. Testing ESG score calculation")

    score = department_esg_score_service.create_score(
        db,
        DepartmentScoreCreate(
            department_id=department.id,
            environmental_score=80,
            social_score=70,
            governance_score=90,
        ),
    )

    expected_total = 80.0

    print("Department score created")
    print("Score ID:", score.id)
    print(
        "Environmental:",
        score.environmental_score,
    )
    print("Social:", score.social_score)
    print("Governance:", score.governance_score)
    print("Calculated total:", score.total_score)
    print("Expected total:", expected_total)

    if score.total_score != expected_total:
        raise AssertionError(
            "Department ESG score calculation is incorrect."
        )


def test_invalid_department(db):
    print("\n4. Testing invalid department handling")

    try:
        department_esg_score_service.create_score(
            db,
            DepartmentScoreCreate(
                department_id=999999,
                environmental_score=80,
                social_score=70,
                governance_score=90,
            ),
        )

    except ValueError as error:
        print(
            "Expected validation error received:",
            error,
        )

    else:
        raise AssertionError(
            "Invalid department was not rejected."
        )


def display_database_records(db):
    print("\n5. Current test records")

    departments = list(
        db.scalars(
            select(Department)
            .order_by(Department.id)
        ).all()
    )

    carbon_transactions = list(
        db.scalars(
            select(CarbonTransaction)
            .order_by(CarbonTransaction.id)
        ).all()
    )

    department_scores = list(
        db.scalars(
            select(DepartmentScore)
            .order_by(DepartmentScore.id)
        ).all()
    )

    print(
        "Departments:",
        len(departments),
    )

    print(
        "Carbon transactions:",
        len(carbon_transactions),
    )

    print(
        "Department scores:",
        len(department_scores),
    )


def main():
    db = SessionLocal()

    try:
        print("=" * 60)
        print("ECOSPHERE PHASE 8 SERVICE TESTS")
        print("=" * 60)

        department = get_or_create_department(db)
        emission_factor = (
            get_or_create_emission_factor(db)
        )

        test_generic_department_service(db)

        test_carbon_service(
            db,
            department,
            emission_factor,
        )

        test_esg_score_service(
            db,
            department,
        )

        test_invalid_department(db)

        display_database_records(db)

        print("\n" + "=" * 60)
        print("ALL PHASE 8 TESTS PASSED")
        print("=" * 60)

    except IntegrityError as error:
        db.rollback()

        print("\nDatabase integrity error:")
        print(error.orig)

    except Exception as error:
        db.rollback()

        print("\nTEST FAILED")
        print("Error type:", type(error).__name__)
        print("Error:", error)

    finally:
        db.close()


if __name__ == "__main__":
    main()