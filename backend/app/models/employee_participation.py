from sqlalchemy import (
    Column,
    Integer,
    String,
    Date,
    ForeignKey
)

from sqlalchemy.orm import relationship

from app.database.base import Base


class EmployeeParticipation(Base):
    __tablename__ = "employee_participations"

    id = Column(Integer, primary_key=True)

    employee_name = Column(String(100), nullable=False)

    csr_activity_id = Column(
        Integer,
        ForeignKey("csr_activities.id")
    )

    proof = Column(String(255))

    approval_status = Column(String(30))

    points_earned = Column(Integer)

    completion_date = Column(Date)

    csr_activity = relationship("CSRActivity")