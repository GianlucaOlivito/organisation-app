import logging
from dataclasses import replace
from uuid import UUID

from app.application.common.calculators import standardize_unit
from app.domain.inventory.inventory_item import InventoryItem

from .repository import InventoryRepository

logger = logging.getLogger(__name__)


class InventoryModificationService:
    """Service for use case UC-3.1: Create, Modify and Delete Inventory Item."""

    def __init__(self, inventory_repository: InventoryRepository) -> None:
        logger.debug("Initialized %s.", self.__class__.__name__)
        self._inventory_repository = inventory_repository

    def create(self, inventory_item: InventoryItem) -> InventoryItem:
        std_new_qty, std_new_unit = standardize_unit(
            inventory_item.quantity, inventory_item.unit
        )
        for existing in self._inventory_repository.get_all():
            existing_qty, existing_unit = standardize_unit(
                existing.quantity, existing.unit
            )
            if (
                existing.name.lower() == inventory_item.name.lower()
                and existing_unit == std_new_unit
            ):
                updated_item = replace(
                    existing,
                    quantity=existing_qty + std_new_qty,
                    unit=std_new_unit,
                )
                self._inventory_repository.save(updated_item)
                logger.info(
                    "Merged %s %s into existing inventory item '%s'.",
                    std_new_qty,
                    std_new_unit,
                    existing.id,
                )
                return updated_item
        item_to_save = replace(inventory_item, quantity=std_new_qty, unit=std_new_unit)
        self._inventory_repository.save(item_to_save)
        logger.info("Created inventory item with ID '%s'.", item_to_save.id)
        return item_to_save

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
