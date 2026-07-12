from sqlalchemy import (
    Column,
    Integer,
    Float,
    String,
    Date,
    ForeignKey,
    DateTime
)
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from app.database.base import Base


class CarbonTransaction(Base):
    __tablename__ = "carbon_transactions"

    id = Column(Integer, primary_key=True, index=True)

    department_id = Column(
        Integer,
        ForeignKey("departments.id"),
        nullable=False
    )

    emission_factor_id = Column(
        Integer,
        ForeignKey("emission_factors.id"),
        nullable=False
    )

    product_profile_id = Column(
        Integer,
        ForeignKey("product_esg_profiles.id"),
        nullable=True
    )

    activity = Column(String(150), nullable=False)

    quantity = Column(Float, nullable=False)

    emission = Column(Float, nullable=False)

    transaction_date = Column(Date, nullable=False)

    created_at = Column(
        DateTime(timezone=True),
        server_default=func.now()
    )

    department = relationship("Department")
    emission_factor = relationship("EmissionFactor")
    product_profile = relationship("ProductESGProfile")