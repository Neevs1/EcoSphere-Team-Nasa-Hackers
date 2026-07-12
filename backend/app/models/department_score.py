from sqlalchemy import (
    Column,
    Integer,
    Float,
    ForeignKey
)

from sqlalchemy.orm import relationship

from app.database.base import Base


class DepartmentScore(Base):
    __tablename__ = "department_scores"

    id = Column(Integer, primary_key=True)

    department_id = Column(
        Integer,
        ForeignKey("departments.id")
    )

    environmental_score = Column(Float)

    social_score = Column(Float)

    governance_score = Column(Float)

    total_score = Column(Float)

    department = relationship("Department")