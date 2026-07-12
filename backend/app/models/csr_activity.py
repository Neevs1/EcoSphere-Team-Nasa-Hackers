from sqlalchemy import (
    Column,
    Integer,
    String,
    Text,
    Date,
    Boolean,
    ForeignKey
)

from sqlalchemy.orm import relationship

from app.database.base import Base


class CSRActivity(Base):
    __tablename__ = "csr_activities"

    id = Column(Integer, primary_key=True)

    title = Column(String(200), nullable=False)

    category_id = Column(
        Integer,
        ForeignKey("categories.id")
    )

    description = Column(Text)

    organizer = Column(String(100))

    activity_date = Column(Date)

    status = Column(Boolean, default=True)

    category = relationship("Category")