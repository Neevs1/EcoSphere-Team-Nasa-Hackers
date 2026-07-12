from sqlalchemy import (
    Column,
    Integer,
    String,
    Date,
    ForeignKey
)

from sqlalchemy.orm import relationship

from app.database.base import Base


class PolicyAcknowledgement(Base):
    __tablename__ = "policy_acknowledgements"

    id = Column(Integer, primary_key=True)

    employee_name = Column(String(100))

    policy_id = Column(
        Integer,
        ForeignKey("esg_policies.id")
    )

    acknowledgement_date = Column(Date)

    status = Column(String(30))

    policy = relationship("ESGPolicy")