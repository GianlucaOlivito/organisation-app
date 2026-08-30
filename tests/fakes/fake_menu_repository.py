from datetime import date
from uuid import UUID

from app.application.meal_planning.repository import MenuRepository
from app.domain.meal_planning.menu import Menu


class FakeMenuRepository(MenuRepository):
    """In-memory implementation of MenuRepository for fast unit testing."""

    def __init__(self) -> None:
        self._menus: dict[UUID, Menu] = {}

    def get_all(self) -> list[Menu]:
        return list(self._menus.values())

    def get_by_id(self, id: UUID) -> Menu | None:
        return self._menus.get(id)

    def filter_by_date_range(self, start_date: date, end_date: date) -> list[Menu]:
        return [
            menu
            for menu in self._menus.values()
            if start_date <= menu.scheduled_date <= end_date
        ]

    def save(self, menu: Menu) -> None:
        self._menus[menu.id] = menu

    def delete(self, id: UUID) -> None:
        self._menus.pop(id, None)
