from sqlalchemy import (
    Column,
    Integer,
    String,
    Date,
    ForeignKey,
    UniqueConstraint,
)
from sqlalchemy.orm import relationship

from app.database.base import Base


class EmployeeParticipation(Base):
    __tablename__ = "employee_participations"

    __table_args__ = (
        UniqueConstraint(
            "employee_id",
            "activity_id",
            name="uq_employee_activity",
        ),
    )

    id = Column(Integer, primary_key=True)

    employee_id = Column(
        Integer,
        ForeignKey("users.id"),
        nullable=False,
    )

    activity_id = Column(
        Integer,
        ForeignKey("csr_activities.id"),
        nullable=False,
    )

    proof_url = Column(String(500))

    approval_status = Column(
        String(30), default="Pending"
    )

    points_earned = Column(Integer, default=0)

    completion_date = Column(Date)

    employee = relationship("User")
    activity = relationship("CSRActivity")