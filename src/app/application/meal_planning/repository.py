from abc import ABC, abstractmethod
from datetime import date
from uuid import UUID

from app.domain.meal_planning.menu import Menu


class MenuRepository(ABC):
    """Repository interface for managing meal planning."""

    @abstractmethod
    def get_all(self) -> list[Menu]: ...

    @abstractmethod
    def get_by_id(self, id: UUID) -> Menu | None: ...

    @abstractmethod
    def filter_by_date_range(self, start_date: date, end_date: date) -> list[Menu]: ...

    @abstractmethod
    def save(self, menu: Menu) -> None: ...

    @abstractmethod
    def delete(self, id: UUID) -> None: ...
