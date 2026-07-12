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


class Challenge(Base):
    __tablename__ = "challenges"

    id = Column(Integer, primary_key=True)

    title = Column(String(200), nullable=False)

    category_id = Column(
        Integer,
        ForeignKey("categories.id")
    )

    description = Column(Text)

    xp = Column(Integer)

    difficulty = Column(String(30))

    evidence_required = Column(Boolean)

    deadline = Column(Date)

    status = Column(String(30))

    category = relationship("Category")