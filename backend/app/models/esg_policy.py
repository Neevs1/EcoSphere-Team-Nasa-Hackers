from sqlalchemy import (
    Column,
    Integer,
    String,
    Text,
    Boolean,
    Date
)

from app.database.base import Base


class ESGPolicy(Base):
    __tablename__ = "esg_policies"

    id = Column(Integer, primary_key=True)

    title = Column(String(200), nullable=False)

    description = Column(Text)

    version = Column(String(20))

    effective_date = Column(Date)

    status = Column(Boolean, default=True)