import logging
from uuid import UUID

from app.domain.inventory.inventory_item import InventoryItem

from .repository import InventoryRepository

logger = logging.getLogger(__name__)


class InventorySearchService:
    """Service for use case UC-3.2: Search Inventory."""

    def __init__(self, inventory_repository: InventoryRepository) -> None:
        self._inventory_repository = inventory_repository
        logger.debug("Initialized %s.", self.__class__.__name__)

    def get_all(self) -> list[InventoryItem]:
        return self._inventory_repository.get_all()

    def get_by_id(self, id: UUID) -> InventoryItem | None:
        return self._inventory_repository.get_by_id(id)

    def get_by_name(self, name: str) -> InventoryItem | None:
        return self._inventory_repository.get_by_name(name)
