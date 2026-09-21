"""Small date utility. SQLite (used in the tests) doesn't keep the
timezone of DateTime(timezone=True) columns - it returns naive datetimes,
unlike Postgres/Neon in production which does return timezone-aware
datetimes. This function makes the two consistent before any comparison,
assuming UTC when the info is missing (that's always what's stored)."""
from datetime import timezone


def ensure_aware_utc(dt):
    if dt.tzinfo is None:
        return dt.replace(tzinfo=timezone.utc)
    return dt
