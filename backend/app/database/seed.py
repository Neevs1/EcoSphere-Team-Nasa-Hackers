"""
Seed script — creates demo users, departments,
and the singleton ESG configuration.

Called at app startup (idempotent).
"""
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.auth.security import hash_password
from app.models.user import User
from app.models.department import Department
from app.models.esg_configuration import (
    EsgConfiguration,
)
from app.models.category import Category


SEED_DEPARTMENTS = [
    {
        "name": "Sustainability",
        "code": "SUST",
        "employee_count": 12,
    },
    {
        "name": "Operations",
        "code": "OPS",
        "employee_count": 45,
    },
    {
        "name": "Human Resources",
        "code": "HR",
        "employee_count": 18,
    },
    {
        "name": "Finance",
        "code": "FIN",
        "employee_count": 22,
    },
    {
        "name": "Marketing",
        "code": "MKT",
        "employee_count": 15,
    },
]

SEED_USERS = [
    {
        "name": "System Admin",
        "email": "admin@ecosphere.dev",
        "password": "admin123",
        "role": "system_admin",
        "department_index": None,
    },
    {
        "name": "ESG Manager",
        "email": "esg@ecosphere.dev",
        "password": "esg123",
        "role": "esg_admin",
        "department_index": 0,
    },
    {
        "name": "Pranav Sharma",
        "email": "pranav@ecosphere.dev",
        "password": "dept123",
        "role": "department_head",
        "department_index": 1,
    },
    {
        "name": "Compliance Officer",
        "email": "compliance@ecosphere.dev",
        "password": "comp123",
        "role": "compliance_officer",
        "department_index": None,
    },
    {
        "name": "Jane Employee",
        "email": "jane@ecosphere.dev",
        "password": "emp123",
        "role": "employee",
        "department_index": 1,
    },
]

SEED_CATEGORIES = [
    {"name": "Tree Planting", "type": "csr_activity"},
    {"name": "Community Cleanup", "type": "csr_activity"},
    {"name": "Education Outreach", "type": "csr_activity"},
    {"name": "Carbon Reduction", "type": "challenge"},
    {"name": "Sustainability Innovation", "type": "challenge"},
    {"name": "Green Office", "type": "challenge"},
]


def seed_database(db: Session) -> None:
    """Idempotent seed — skips if data exists."""

    existing = db.scalars(
        select(User).limit(1)
    ).first()

    if existing is not None:
        return

    # --- Departments ---
    departments = []
    for dept_data in SEED_DEPARTMENTS:
        dept = Department(**dept_data)
        db.add(dept)
        departments.append(dept)

    db.flush()

    # --- Users ---
    for user_data in SEED_USERS:
        dept_idx = user_data.pop(
            "department_index"
        )
        password = user_data.pop("password")

        user = User(
            name=user_data["name"],
            email=user_data["email"],
            password_hash=hash_password(password),
            role=user_data["role"],
            department_id=(
                departments[dept_idx].id
                if dept_idx is not None
                else None
            ),
        )
        db.add(user)

    # --- ESG Configuration singleton ---
    esg_config = EsgConfiguration(
        id=1,
        auto_emission_calculation=False,
        require_evidence_for_csr=False,
        environmental_weight=0.40,
        social_weight=0.30,
        governance_weight=0.30,
    )
    db.add(esg_config)

    # --- Categories ---
    for cat_data in SEED_CATEGORIES:
        db.add(Category(**cat_data))

    db.commit()
    print("✓ Database seeded successfully.")
