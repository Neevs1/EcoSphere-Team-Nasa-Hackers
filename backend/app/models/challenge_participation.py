from sqlalchemy import (
    Column,
    Integer,
    String,
    ForeignKey,
    UniqueConstraint,
)
from sqlalchemy.orm import relationship

from app.database.base import Base


class ChallengeParticipation(Base):
    __tablename__ = "challenge_participations"

    __table_args__ = (
        UniqueConstraint(
            "challenge_id",
            "employee_id",
            name="uq_challenge_employee",
        ),
    )

    id = Column(Integer, primary_key=True)

    challenge_id = Column(
        Integer,
        ForeignKey("challenges.id"),
    )

    employee_id = Column(
        Integer,
        ForeignKey("users.id"),
    )

    progress = Column(Integer, default=0)

    proof_url = Column(String(500))

    approval_status = Column(
        String(30), default="Pending"
    )

    xp_awarded = Column(Integer, default=0)

    challenge = relationship("Challenge")
    employee = relationship("User")