from uuid import UUID

from app.application.inventory.repository import InventoryRepository
from app.domain.inventory.inventory_item import InventoryItem


class FakeInventoryRepository(InventoryRepository):
    """In-memory implementation of InventoryRepository for fast unit testing."""

    def __init__(self) -> None:
        self._inventory: dict[UUID, InventoryItem] = {}

    def get_all(self) -> list[InventoryItem]:
        return list(self._inventory.values())

    def get_by_id(self, id: UUID) -> InventoryItem | None:
        return self._inventory.get(id)

    def get_by_name(self, name: str) -> InventoryItem | None:
        return next((i for i in self._inventory.values() if i.name == name), None)

    def save(self, item: InventoryItem) -> None:
        self._inventory[item.id] = item

    def delete(self, id: UUID) -> None:
        self._inventory.pop(id, None)
