import logging
from pathlib import Path
from typing import Any
from uuid import UUID

from app.adapters.common.json_base_repository import JsonBaseRepository
from app.application.inventory.repository import InventoryRepository
from app.config.settings import settings
from app.domain.inventory.inventory_item import InventoryItem

logger = logging.getLogger(__name__)


class JsonInventoryRepository(JsonBaseRepository[InventoryItem], InventoryRepository):
    """Implementation part of UC-3.1 and UC-3.2: Manage inventory persistence with JSON."""

    def __init__(self, file_path: Path | None = None) -> None:
        super().__init__(file_path=file_path or settings.inventory_file_path)

    def _entity_to_dict(self, entity: InventoryItem) -> dict[str, Any]:
        return {
            "id": str(entity.id),
            "name": entity.name,
            "quantity": entity.quantity,
            "unit": entity.unit,
        }

    def _dict_to_entity(self, data: dict[str, Any]) -> InventoryItem:
        return InventoryItem(
            id=UUID(data["id"]),
            name=data["name"],
            quantity=data["quantity"],
            unit=data["unit"],
        )

    def get_by_name(self, name: str) -> InventoryItem | None:
        normalized_name = name.strip().lower()
        inventory_item = next(
            (i for i in self.get_all() if i.name.strip().lower() == normalized_name),
            None,
        )
        if inventory_item:
            logger.debug("Found entity with name '%s'.", name)
        else:
            logger.debug("Failed to find entity with name '%s'.", name)
        return inventory_item
