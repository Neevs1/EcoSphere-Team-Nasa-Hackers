from sqlalchemy import text

from app.database.db import engine


def test_database_connection() -> None:
    """
    Verify that the application can connect to PostgreSQL.

    Database tables are created and updated through Alembic migrations.
    """

    with engine.connect() as connection:
        result = connection.execute(text("SELECT 1"))
        value = result.scalar_one()

        if value != 1:
            raise RuntimeError("Unexpected PostgreSQL response.")


if __name__ == "__main__":
    test_database_connection()
    print("PostgreSQL connection successful.")