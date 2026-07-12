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


class OperationalRecord(Base):
    __tablename__ = "operational_records"

    id = Column(Integer, primary_key=True, index=True)

    department_id = Column(
        Integer,
        ForeignKey("departments.id"),
        nullable=False,
    )

    source_type = Column(
        String(30), nullable=False
    )

    quantity = Column(Float, nullable=False)

    emission_factor_id = Column(
        Integer,
        ForeignKey("emission_factors.id"),
        nullable=False,
    )

    created_at = Column(
        DateTime(timezone=True),
        server_default=func.now(),
    )

    department = relationship("Department")
    emission_factor = relationship("EmissionFactor")
