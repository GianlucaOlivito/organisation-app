from datetime import date, datetime
from uuid import UUID


def parse_str_to_uuid(value: str) -> UUID | None:
    if not value:
        return None
    try:
        return UUID(value)
    except ValueError:
        return None


def parse_str_to_date(value: date | str | None) -> date | None:
    if isinstance(value, date):
        return value
    if not value or not value.strip():
        return None
    for fmt in ("%d.%m.%Y", "%Y-%m-%d"):
        try:
            return datetime.strptime(value.strip(), fmt).date()  # noqa: DTZ007
        except ValueError:
            continue
    return None
