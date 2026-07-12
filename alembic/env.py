import os
import sys
from logging.config import fileConfig

from alembic import context
from dotenv import load_dotenv
from sqlalchemy import engine_from_config, pool

# ---------------------------------------------------------
# Paths
# ---------------------------------------------------------

# Project root:
# nasa-hacker-o/
project_root = os.path.abspath(
    os.path.join(os.path.dirname(__file__), "..")
)

# Backend folder:
# nasa-hacker-o/backend/
backend_path = os.path.join(project_root, "backend")

# Add backend to Python path so imports such as
# from app.database.base import Base work correctly.
sys.path.insert(0, backend_path)

# ---------------------------------------------------------
# Load environment variables
# ---------------------------------------------------------

# Load:
# nasa-hacker-o/backend/.env
env_path = os.path.join(backend_path, ".env")
load_dotenv(env_path)

# ---------------------------------------------------------
# Alembic configuration
# ---------------------------------------------------------

config = context.config

if config.config_file_name is not None:
    fileConfig(config.config_file_name)

database_url = os.getenv("DATABASE_URL")

if not database_url:
    raise ValueError(
        f"DATABASE_URL is missing. Add it to: {env_path}"
    )

# Escape percent signs because Alembic uses ConfigParser internally.
config.set_main_option(
    "sqlalchemy.url",
    database_url.replace("%", "%%")
)

# ---------------------------------------------------------
# Import SQLAlchemy Base and models
# ---------------------------------------------------------

from app.database.base import Base

from app.models import (
    Department,
    Category,
    EmissionFactor,
    ProductESGProfile,
    EnvironmentalGoal,
    ESGPolicy,
    Badge,
    Reward,
    CarbonTransaction,
    CSRActivity,
    EmployeeParticipation,
    Challenge,
    ChallengeParticipation,
    PolicyAcknowledgement,
    Audit,
    ComplianceIssue,
    DepartmentScore,
)

# Alembic reads this metadata to discover all database tables.
target_metadata = Base.metadata


def run_migrations_offline() -> None:
    """
    Run migrations without creating a database connection.
    """

    url = config.get_main_option("sqlalchemy.url")

    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={
            "paramstyle": "named",
        },
        compare_type=True,
        compare_server_default=True,
    )

    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online() -> None:
    """
    Run migrations using a live PostgreSQL database connection.
    """

    configuration = config.get_section(
        config.config_ini_section,
        {}
    )

    connectable = engine_from_config(
        configuration,
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )

    with connectable.connect() as connection:
        context.configure(
            connection=connection,
            target_metadata=target_metadata,
            compare_type=True,
            compare_server_default=True,
        )

        with context.begin_transaction():
            context.run_migrations()


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()

