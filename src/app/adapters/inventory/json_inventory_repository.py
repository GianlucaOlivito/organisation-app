import logging
from pathlib import Path
from typing import Any
from uuid import UUID

from app.adapters.common.json_file_handler import read_json_file, write_json_file
from app.application.inventory.repository import InventoryRepository
from app.config.settings import settings
from app.domain.inventory.inventory_item import InventoryItem

logger = logging.getLogger(__name__)


class JsonInventoryRepository(InventoryRepository):
    """Implementation part of UC-3.1 and UC-3.2: Manage inventory persistence with JSON."""

    def __init__(self, file_path: Path | None = None) -> None:
        self._file_path = file_path or settings.inventory_file_path
        logger.debug(
            "JsonInventoryRepository initialized with path: %s", self._file_path
        )

    def _inventory_item_to_dict(self, item: InventoryItem) -> dict[str, Any]:
        return {
            "id": str(item.id),
            "name": item.name,
            "quantity": item.quantity,
            "unit": item.unit,
        }

    def _dict_to_inventory_item(self, data: dict[str, Any]) -> InventoryItem:
        return InventoryItem(
            id=UUID(data["id"]),
            name=data["name"],
            quantity=data["quantity"],
            unit=data["unit"],
        )

    def get_all(self) -> list[InventoryItem]:
        raw_data = read_json_file(self._file_path)
        inventory: list[InventoryItem] = []
        for item in raw_data:
            try:
                inventory.append(self._dict_to_inventory_item(item))
            except (KeyError, ValueError, TypeError) as e:
                logger.error("Skipping invalid inventory item: %s. Error: %s", item, e)
        logger.debug(
            "Retrieved %d inventory items from %s.", len(inventory), self._file_path
        )
        return inventory

    def get_by_id(self, id: UUID) -> InventoryItem | None:
        inventory_item = next((i for i in self.get_all() if i.id == id), None)
        if inventory_item:
            logger.debug("Found inventory item with ID '%s'.", id)
        else:
            logger.debug("No inventory item found with ID '%s'.", id)
        return inventory_item

    def get_by_name(self, name: str) -> InventoryItem | None:
        normalized_name = name.strip().lower()
        inventory_item = next(
            (i for i in self.get_all() if i.name.strip().lower() == normalized_name),
            None,
        )
        if inventory_item:
            logger.debug("Found inventory item with name '%s'.", name)
        else:
            logger.debug("No inventory item found with name '%s'.", name)
        return inventory_item

    def save(self, inventory_item: InventoryItem) -> None:
        inventory = self.get_all()
        updated = False
        for idx, existing in enumerate(inventory):
            if existing.id == inventory_item.id:
                inventory[idx] = inventory_item
                updated = True
                break
        if not updated:
            inventory.append(inventory_item)
        serialized = [self._inventory_item_to_dict(i) for i in inventory]
        write_json_file(self._file_path, serialized)
        logger.info(
            "Saved inventory item '%s' (ID: %s) to '%s'.",
            inventory_item.name,
            inventory_item.id,
            self._file_path,
        )

    def delete(self, id: UUID) -> None:
        inventory = self.get_all()
        filtered = [i for i in inventory if i.id != id]
        if len(filtered) != len(inventory):
            serialized = [self._inventory_item_to_dict(i) for i in filtered]
            write_json_file(self._file_path, serialized)
            logger.info(
                "Deleted inventory item with ID '%s' from '%s'.", id, self._file_path
            )
        else:
            logger.warning(
                "Attempted to delete non-existent inventory item with ID '%s'.", id
            )
