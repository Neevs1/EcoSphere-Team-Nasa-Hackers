from sqlalchemy import (
    Column,
    Integer,
    DateTime,
    ForeignKey,
)
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from app.database.base import Base


class RewardRedemption(Base):
    __tablename__ = "reward_redemptions"

    id = Column(Integer, primary_key=True, index=True)

    employee_id = Column(
        Integer,
        ForeignKey("users.id"),
        nullable=False,
    )

    reward_id = Column(
        Integer,
        ForeignKey("rewards.id"),
        nullable=False,
    )

    points_deducted = Column(Integer, nullable=False)

    redeemed_at = Column(
        DateTime(timezone=True),
        server_default=func.now(),
    )

    employee = relationship("User")
    reward = relationship("Reward")
