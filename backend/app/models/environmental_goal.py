from sqlalchemy import (
    Column,
    Integer,
    String,
    Float,
    Date,
    Boolean,
    ForeignKey,
)
from sqlalchemy.orm import relationship

from app.database.base import Base


class EnvironmentalGoal(Base):
    __tablename__ = "environmental_goals"

    id = Column(Integer, primary_key=True)

    department_id = Column(
        Integer,
        ForeignKey("departments.id"),
    )

    name = Column(String(200), nullable=False)

    target_co2 = Column(Float)

    current_co2 = Column(Float, default=0.0)

    deadline = Column(Date)

    status = Column(Boolean, default=True)

    department = relationship("Department")