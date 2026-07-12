from sqlalchemy import (
    Column,
    Integer,
    String,
    Text,
    Boolean
)

from app.database.base import Base


class Reward(Base):
    __tablename__ = "rewards"

    id = Column(Integer, primary_key=True)

    name = Column(String(100), nullable=False)

    description = Column(Text)

    points_required = Column(Integer, nullable=False)

    stock = Column(Integer, default=0)

    status = Column(Boolean, default=True)