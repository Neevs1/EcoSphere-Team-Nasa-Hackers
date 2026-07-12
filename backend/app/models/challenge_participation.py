from sqlalchemy import (
    Column,
    Integer,
    String,
    ForeignKey
)

from sqlalchemy.orm import relationship

from app.database.base import Base


class ChallengeParticipation(Base):
    __tablename__ = "challenge_participations"

    id = Column(Integer, primary_key=True)

    challenge_id = Column(
        Integer,
        ForeignKey("challenges.id")
    )

    employee_name = Column(String(100))

    progress = Column(Integer)

    proof = Column(String(255))

    approval = Column(String(30))

    xp_awarded = Column(Integer)

    challenge = relationship("Challenge")