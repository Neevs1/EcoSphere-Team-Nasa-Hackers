from sqlalchemy import (
    Column,
    Integer,
    String,
    Float,
    Date,
    Boolean,
    ForeignKey
)

from sqlalchemy.orm import relationship

from app.database.base import Base


class EnvironmentalGoal(Base):
    __tablename__ = "environmental_goals"

    id = Column(Integer, primary_key=True)

    department_id = Column(
        Integer,
        ForeignKey("departments.id")
    )

    goal_name = Column(String(200), nullable=False)

    target_value = Column(Float)

    achieved_value = Column(Float)

    target_date = Column(Date)

    status = Column(Boolean, default=True)

    department = relationship("Department")