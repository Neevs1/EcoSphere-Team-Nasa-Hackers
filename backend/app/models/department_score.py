from sqlalchemy import (
    Column,
    Integer,
    Float,
    String,
    DateTime,
    ForeignKey,
)
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from app.database.base import Base


class DepartmentScore(Base):
    __tablename__ = "department_scores"

    id = Column(Integer, primary_key=True)

    department_id = Column(
        Integer,
        ForeignKey("departments.id"),
    )

    period = Column(String(20))

    environmental_score = Column(Float)

    social_score = Column(Float)

    governance_score = Column(Float)

    total_score = Column(Float)

    computed_at = Column(
        DateTime(timezone=True),
        server_default=func.now(),
    )

    department = relationship("Department")