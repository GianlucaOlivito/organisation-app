import logging
from uuid import UUID

from app.domain.inventory.inventory_item import InventoryItem

from .repository import InventoryRepository

logger = logging.getLogger(__name__)


class InventoryModificationService:
    """Service for use case UC-3.1: Create, Modify and Delete Inventory Item."""

    def __init__(self, inventory_repository: InventoryRepository) -> None:
        logger.debug("Initialized %s.", self.__class__.__name__)
        self._inventory_repository = inventory_repository

    def create(self, inventory_item: InventoryItem) -> InventoryItem:
        if self._inventory_repository.get_by_id(inventory_item.id):
            logger.warning(
                "Failed to create existing inventory item with ID '%s'.",
                inventory_item.id,
            )
            raise ValueError(
                f"INVALID ARGUMENT: Inventory item with ID '{inventory_item.id}' already exists."
            )
        self._inventory_repository.save(inventory_item)
        logger.info("Created inventory item with ID '%s'.", inventory_item.id)
        return inventory_item

    def modify(self, inventory_item: InventoryItem) -> None:
        if not self._inventory_repository.get_by_id(inventory_item.id):
            logger.warning(
                "Failed to modify non-existent inventory item with ID '%s'.",
                inventory_item.id,
            )
            raise ValueError(
                f"INVALID ARGUMENT: Inventory item with ID '{inventory_item.id}' does not exist."
            )
        self._inventory_repository.save(inventory_item)
        logger.info("Modified inventory item with ID '%s'.", inventory_item.id)

    def delete(self, id: UUID) -> None:
        if not self._inventory_repository.get_by_id(id):
            logger.warning(
                "Failed to delete non-existent inventory item with ID '%s'.", id
            )
            raise ValueError(
                f"INVALID ARGUMENT: Inventory item with ID '{id}' does not exist."
            )
        self._inventory_repository.delete(id)
        logger.info("Deleted inventory item with ID '%s'.", id)
