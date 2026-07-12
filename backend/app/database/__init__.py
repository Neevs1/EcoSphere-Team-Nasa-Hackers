from app.database.base import Base
from app.database.db import engine

# Import all models
from app.models import *

def create_database():
    Base.metadata.create_all(bind=engine)

if __name__ == "__main__":
    create_database()
    print("Database created successfully!")