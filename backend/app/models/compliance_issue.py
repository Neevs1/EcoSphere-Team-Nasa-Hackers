from sqlalchemy import (
    Column,
    Integer,
    String,
    Text,
    Date,
    ForeignKey,
)
from sqlalchemy.orm import relationship

from app.database.base import Base


class ComplianceIssue(Base):
    __tablename__ = "compliance_issues"

    id = Column(Integer, primary_key=True)

    audit_id = Column(
        Integer,
        ForeignKey("audits.id"),
    )

    severity = Column(String(30), nullable=False)

    description = Column(Text)

    owner_id = Column(
        Integer,
        ForeignKey("users.id"),
        nullable=False,
    )

    department_id = Column(
        Integer,
        ForeignKey("departments.id"),
    )

    due_date = Column(Date, nullable=False)

    status = Column(
        String(30), default="Open"
    )

    audit = relationship("Audit")
    owner = relationship("User")
    department = relationship("Department")