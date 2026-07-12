from sqlalchemy import Column, Integer, String, Text

from app.database.base import Base


class Badge(Base):
    __tablename__ = "badges"

    id = Column(Integer, primary_key=True)

    name = Column(String(100), nullable=False)

    description = Column(Text)

    unlock_rule = Column(Text)

    icon = Column(String(255))