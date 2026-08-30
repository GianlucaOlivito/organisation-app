import logging
from uuid import UUID

from app.domain.meal_planning.menu import Menu

from .repository import MenuRepository

logger = logging.getLogger(__name__)


class MenuModificationService:
    """Service for use case UC-2.1: Create, Modify and Delete Menu."""

    def __init__(self, menu_repository: MenuRepository) -> None:
        logger.debug("MenuModificationService initialized.")
        self._menu_repository = menu_repository

    def create(self, menu: Menu) -> Menu:
        if self._menu_repository.get_by_id(menu.id):
            logger.warning(
                f"Menu creation failed: Menu with ID '{menu.id}' already exists."
            )
            raise ValueError(
                f"INVALID ARGUMENT: Menu with ID '{menu.id}' already exists."
            )
        self._menu_repository.save(menu)
        logger.info(f"Menu created: ID {menu.id}")
        return menu

    def modify(self, menu: Menu) -> None:
        if not self._menu_repository.get_by_id(menu.id):
            logger.warning(
                f"Menu modification failed: Menu with ID '{menu.id}' does not exist."
            )
            raise ValueError(
                f"INVALID ARGUMENT: Menu with ID '{menu.id}' does not exist."
            )
        self._menu_repository.save(menu)
        logger.info(f"Menu with ID '{menu.id}' modified.")

    def delete(self, id: UUID) -> None:
        if not self._menu_repository.get_by_id(id):
            logger.warning(f"Menu deletion failed: Menu with ID '{id}' does not exist.")
            raise ValueError(f"INVALID ARGUMENT: Menu with ID '{id}' does not exist.")
        self._menu_repository.delete(id)
        logger.info(f"Menu with ID '{id}' deleted.")
