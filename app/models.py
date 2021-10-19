from datetime import datetime, timezone

from sqlalchemy import Column, DateTime


def now() -> datetime:
    """Returns the current timezone-aware UTC timestamp."""
    return datetime.now(timezone.utc)


class TimestampMixin:
    """Adds created and updated at timestamps to a model"""
    created_at = Column(DateTime(timezone=True), nullable=False, default=now)
    updated_at = Column(DateTime(timezone=True), onupdate=now)
