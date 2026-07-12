from sqlalchemy import (
    Column,
    Integer,
    String,
    Text,
    Date,
    ForeignKey
)

from sqlalchemy.orm import relationship

from app.database.base import Base


class ComplianceIssue(Base):
    __tablename__ = "compliance_issues"

    id = Column(Integer, primary_key=True)

    audit_id = Column(
        Integer,
        ForeignKey("audits.id")
    )

    severity = Column(String(30))

    description = Column(Text)

    owner = Column(String(100))

    due_date = Column(Date)

    status = Column(String(30))

    audit = relationship("Audit")