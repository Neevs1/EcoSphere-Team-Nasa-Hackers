from fastapi import FastAPI
from sqlalchemy import text

from app.database.db import engine

app = FastAPI(
    title="EcoSphere ESG Management Platform",
    description="Backend API for ESG Management Platform",
    version="1.0.0"
)


@app.get("/")
def root():
    return {
        "message": "EcoSphere Backend is running successfully!"
    }


@app.get("/db-test")
def db_test():
    """
    Test PostgreSQL connection.
    """
    with engine.connect() as connection:
        result = connection.execute(text("SELECT 1"))
        return {
            "database": "Connected",
            "result": result.scalar()
        }