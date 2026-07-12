from sqlalchemy import (
    Column,
    Integer,
    String,
    Text,
    Boolean,
)
from sqlalchemy.dialects.postgresql import JSON

from app.database.base import Base


class Badge(Base):
    __tablename__ = "badges"

    id = Column(Integer, primary_key=True)

    name = Column(String(100), nullable=False)

    description = Column(Text)

    unlock_rule = Column(JSON)

    icon_url = Column(String(500))

    status = Column(Boolean, default=True)