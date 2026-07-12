from sqlalchemy import (
    Column,
    Integer,
    Float,
    Boolean,
)

from app.database.base import Base


class EsgConfiguration(Base):
    __tablename__ = "esg_configurations"

    id = Column(Integer, primary_key=True, default=1)

    auto_emission_calculation = Column(
        Boolean, default=False
    )

    require_evidence_for_csr = Column(
        Boolean, default=False
    )

    environmental_weight = Column(
        Float, nullable=False, default=0.40
    )

    social_weight = Column(
        Float, nullable=False, default=0.30
    )

    governance_weight = Column(
        Float, nullable=False, default=0.30
    )
