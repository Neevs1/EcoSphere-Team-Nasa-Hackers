from sqlalchemy import Column, Integer, String, Boolean, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from app.database.base import Base


class Department(Base):
    __tablename__ = "departments"

    id = Column(Integer, primary_key=True, index=True)

    name = Column(String(100), nullable=False, unique=True)

    code = Column(String(20), nullable=False, unique=True)

    head = Column(String(100), nullable=True)

    parent_department_id = Column(
        Integer,
        ForeignKey("departments.id"),
        nullable=True
    )

    employee_count = Column(Integer, default=0)

    status = Column(Boolean, default=True)

    created_at = Column(
        DateTime(timezone=True),
        server_default=func.now()
    )

    updated_at = Column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now()
    )

    parent_department = relationship(
        "Department",
        remote_side=[id]
    )

    child_departments = relationship(
        "Department"
    )