from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy import text

from app.database.base import Base
from app.database.db import engine, SessionLocal
from app.database.seed import seed_database
from app.routers.auth import auth_router
from app.routers.settings import settings_router
from app.routers.environmental import (
    environmental_router,
)
from app.routers.social import social_router
from app.routers.governance import (
    governance_router,
)
from app.routers.gamification import (
    gamification_router,
)
from app.routers.dashboard import dashboard_router
from app.routers.notifications import (
    notifications_router,
)
from app.routers.users import users_router
from app.routers import api_router

# Import all models so Base.metadata knows them
import app.models  # noqa: F401


@asynccontextmanager
async def lifespan(application: FastAPI):
    """Create tables + seed on startup."""
    Base.metadata.create_all(bind=engine)

    db = SessionLocal()
    try:
        seed_database(db)
    finally:
        db.close()

    yield


app = FastAPI(
    title="EcoSphere ESG Management Platform",
    description=(
        "Backend API for Environmental, Social and "
        "Governance management."
    ),
    version="1.0.0",
    lifespan=lifespan,
)

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get(
    "/",
    tags=["System"],
    summary="Backend health check",
)
def root():
    return {
        "message": (
            "EcoSphere Backend is running "
            "successfully."
        )
    }


@app.get(
    "/db-test",
    tags=["System"],
    summary="Test PostgreSQL connection",
)
def db_test():
    with engine.connect() as connection:
        result = connection.execute(
            text("SELECT 1")
        )
        return {
            "database": "Connected",
            "result": result.scalar_one(),
        }


# --- Mount Routers ---

# Auth
app.include_router(
    auth_router, prefix="/api/v1"
)

# Users
app.include_router(
    users_router, prefix="/api/v1"
)

# Settings
app.include_router(
    settings_router, prefix="/api/v1"
)

# Domain routers (Sprints 3-6)
app.include_router(
    environmental_router, prefix="/api/v1"
)
app.include_router(
    social_router, prefix="/api/v1"
)
app.include_router(
    governance_router, prefix="/api/v1"
)
app.include_router(
    gamification_router, prefix="/api/v1"
)

# Dashboard & Reports (Sprint 7)
app.include_router(
    dashboard_router, prefix="/api/v1"
)

# Notifications (Sprint 8)
app.include_router(
    notifications_router, prefix="/api/v1"
)

# Generic CRUD (Sprint -1/2)
app.include_router(
    api_router, prefix="/api/v1"
)