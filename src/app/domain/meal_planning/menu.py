from dataclasses import dataclass, field
from datetime import date
from uuid import UUID, uuid4

from .course import Course


@dataclass(kw_only=True, slots=True)
class Menu:
    """Represents a menu for a date with its courses and unique identifier."""

    id: UUID = field(default_factory=uuid4)
    description: str
    scheduled_date: date
    courses: list[Course] = field(default_factory=list)
