from sqlalchemy import (
    Column,
    Integer,
    String,
    DateTime,
    ForeignKey,
)
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from app.database.base import Base


class Notification(Base):
    __tablename__ = "notifications"

    id = Column(Integer, primary_key=True, index=True)

    recipient_id = Column(
        Integer,
        ForeignKey("users.id"),
        nullable=False,
    )

    type = Column(String(50), nullable=False)

    message = Column(String(500), nullable=False)

    priority = Column(
        String(20),
        nullable=False,
        default="Informational",
    )

    related_entity_type = Column(
        String(50), nullable=True
    )

    related_entity_id = Column(
        Integer, nullable=True
    )

    read_at = Column(
        DateTime(timezone=True), nullable=True
    )

    created_at = Column(
        DateTime(timezone=True),
        server_default=func.now(),
    )

    recipient = relationship("User")
