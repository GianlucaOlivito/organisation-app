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
        logger.debug("MenuSearchService initialized.")

    def get_all(self) -> list[Menu]:
        logger.debug("Fetched all available menus.")
        return self._menu_repository.get_all()

    def get_by_id(self, id: UUID) -> Menu | None:
        logger.debug(f"Fetched menu with ID {id}.")
        return self._menu_repository.get_by_id(id)

    def filter_by_date_range(self, start_date: date, end_date: date) -> list[Menu]:
        logger.debug(f"Filtered menus by date range: from {start_date} to {end_date}")
        return self._menu_repository.filter_by_date_range(start_date, end_date)
