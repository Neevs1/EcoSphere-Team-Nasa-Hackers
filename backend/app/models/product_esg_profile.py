from sqlalchemy import Column, Integer, String, Float, Boolean, DateTime
from sqlalchemy.sql import func

from app.database.base import Base


class ProductESGProfile(Base):
    __tablename__ = "product_esg_profiles"

    id = Column(Integer, primary_key=True)

    product_code = Column(String(50), unique=True, nullable=False)

    product_name = Column(String(150), nullable=False)

    sustainability_score = Column(Float)

    carbon_rating = Column(Float)

    recyclable = Column(Boolean, default=False)

    created_at = Column(
        DateTime(timezone=True),
        server_default=func.now()
    )

    updated_at = Column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now()
    )