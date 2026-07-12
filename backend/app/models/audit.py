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


class Audit(Base):
    __tablename__ = "audits"

    id = Column(Integer, primary_key=True)

    department_id = Column(
        Integer,
        ForeignKey("departments.id")
    )

    audit_name = Column(String(150))

    auditor = Column(String(100))

    audit_date = Column(Date)

    remarks = Column(Text)

    status = Column(String(30))

    department = relationship("Department")