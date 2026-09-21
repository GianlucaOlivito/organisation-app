import logging
from datetime import date
from uuid import UUID

from app.domain.meal_planning.menu import Menu

from .repository import MenuRepository

logger = logging.getLogger(__name__)


class MenuSearchService:
    """Service for use case UC-2.2: Search and Filter Menus."""

    def __init__(self, menu_repository: MenuRepository) -> None:
        self._menu_repository = menu_repository
        logger.debug("Initialized %s.", self.__class__.__name__)

    def get_all(self) -> list[Menu]:
        return self._menu_repository.get_all()

    def get_by_id(self, id: UUID) -> Menu | None:
        return self._menu_repository.get_by_id(id)

    def filter_by_date_range(self, start_date: date, end_date: date) -> list[Menu]:
        return self._menu_repository.filter_by_date_range(start_date, end_date)
