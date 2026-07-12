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


class Audit(Base):
    __tablename__ = "audits"

    id = Column(Integer, primary_key=True)

    title = Column(String(200), nullable=False)

    department_id = Column(
        Integer,
        ForeignKey("departments.id"),
    )

    auditor_id = Column(
        Integer,
        ForeignKey("users.id"),
    )

    audit_date = Column(Date)

    findings_summary = Column(Text)

    status = Column(String(30), default="active")

    department = relationship("Department")
    auditor = relationship("User")