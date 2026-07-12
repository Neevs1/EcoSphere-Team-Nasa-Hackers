from app.database.base import Base
from app.database.db import engine


def create_database():
    """
    Creates all database tables defined by SQLAlchemy models.
    """
    Base.metadata.create_all(bind=engine)


if __name__ == "__main__":
    create_database()
    print("Database tables created successfully.")