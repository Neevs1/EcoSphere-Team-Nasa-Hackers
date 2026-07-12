"""
Sprint 8 — Notifications (in-app only)
"""
from datetime import datetime, timezone

from fastapi import (
    APIRouter,
    Depends,
    HTTPException,
    Query,
)
from pydantic import BaseModel
from sqlalchemy import select, func as sa_func
from sqlalchemy.orm import Session

from app.auth.dependencies import get_current_user
from app.database.db import get_db
from app.models.notification import Notification
from app.models.user import User


notifications_router = APIRouter(
    prefix="/notifications",
    tags=["Notifications"],
)


class NotificationOut(BaseModel):
    id: int
    type: str
    message: str
    priority: str
    related_entity_type: str | None = None
    related_entity_id: int | None = None
    read_at: str | None = None
    created_at: str | None = None
    model_config = {"from_attributes": True}


class UnreadCount(BaseModel):
    count: int


@notifications_router.get(
    "",
    response_model=list[NotificationOut],
    summary="Get user's notifications",
)
def list_notifications(
    unread: bool | None = None,
    skip: int = Query(0, ge=0),
    limit: int = Query(50, ge=1, le=200),
    db: Session = Depends(get_db),
    current_user: User = Depends(
        get_current_user
    ),
):
    stmt = select(Notification).where(
        Notification.recipient_id
        == current_user.id
    )

    if unread:
        stmt = stmt.where(
            Notification.read_at.is_(None)
        )

    stmt = (
        stmt.order_by(
            Notification.created_at.desc()
        )
        .offset(skip)
        .limit(limit)
    )

    return list(db.scalars(stmt).all())


@notifications_router.get(
    "/unread-count",
    response_model=UnreadCount,
    summary="Get unread count",
)
def unread_count(
    db: Session = Depends(get_db),
    current_user: User = Depends(
        get_current_user
    ),
):
    count = db.scalar(
        select(
            sa_func.count(Notification.id)
        ).where(
            Notification.recipient_id
            == current_user.id,
            Notification.read_at.is_(None),
        )
    ) or 0

    return UnreadCount(count=count)


@notifications_router.patch(
    "/{notification_id}/read",
    response_model=NotificationOut,
    summary="Mark notification as read",
)
def mark_read(
    notification_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(
        get_current_user
    ),
):
    notif = db.get(Notification, notification_id)

    if notif is None:
        raise HTTPException(
            404, "Notification not found."
        )

    if notif.recipient_id != current_user.id:
        raise HTTPException(
            403, "Not your notification."
        )

    notif.read_at = datetime.now(timezone.utc)
    db.commit()
    db.refresh(notif)
    return notif
