from sqlalchemy import (
    Column,
    Integer,
    DateTime,
    ForeignKey,
    UniqueConstraint,
)
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from app.database.base import Base


class EmployeeBadge(Base):
    __tablename__ = "employee_badges"

    __table_args__ = (
        UniqueConstraint(
            "employee_id",
            "badge_id",
            name="uq_employee_badge",
        ),
    )

    id = Column(Integer, primary_key=True, index=True)

    employee_id = Column(
        Integer,
        ForeignKey("users.id"),
        nullable=False,
    )

    badge_id = Column(
        Integer,
        ForeignKey("badges.id"),
        nullable=False,
    )

    awarded_at = Column(
        DateTime(timezone=True),
        server_default=func.now(),
    )

    employee = relationship("User")
    badge = relationship("Badge")
