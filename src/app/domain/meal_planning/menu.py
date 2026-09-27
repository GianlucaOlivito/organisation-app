from dataclasses import dataclass, field
from datetime import date
from uuid import UUID, uuid4

from .course import Course


@dataclass(kw_only=True, slots=True)
class Menu:
    """Represents a menu for a date with its courses and unique identifier."""

    id: UUID = field(default_factory=uuid4)
    description: str
    scheduled_date: date | str
    courses: list[Course] = field(default_factory=list)

    def __post_init__(self) -> None:
        if not (self.description or "").strip():
            raise ValueError("Ungültige Menübeschreibung")
        if isinstance(self.scheduled_date, str):
            try:
                scheduled_date = date.fromisoformat(self.scheduled_date.strip())
            except AttributeError, TypeError, ValueError:
                raise TypeError("Ungültiges Datum")
        elif isinstance(self.scheduled_date, date):
            scheduled_date = self.scheduled_date
        else:
            raise TypeError("Ungültiges Datum")
        if not self.courses:
            raise ValueError("Ungültige Gangliste")
        self.description = self.description.strip()
        self.scheduled_date = scheduled_date
