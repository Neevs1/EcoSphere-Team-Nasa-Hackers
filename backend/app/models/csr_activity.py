from sqlalchemy import (
    Column,
    Integer,
    String,
    Text,
    Date,
    Boolean,
    ForeignKey,
)
from sqlalchemy.orm import relationship

from app.database.base import Base


class CSRActivity(Base):
    __tablename__ = "csr_activities"

    id = Column(Integer, primary_key=True)

    title = Column(String(200), nullable=False)

    category_id = Column(
        Integer,
        ForeignKey("categories.id"),
    )

    description = Column(Text)

    points = Column(Integer, default=0)

    evidence_required = Column(
        Boolean, default=False
    )

    status = Column(
        String(30), default="Draft"
    )

    start_date = Column(Date)

    end_date = Column(Date)

    created_at = Column(Date)

    category = relationship("Category")