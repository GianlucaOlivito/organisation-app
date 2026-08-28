from abc import ABC, abstractmethod
from uuid import UUID

from app.domain.inventory.inventory_item import InventoryItem


class InventoryRepository(ABC):
    """Repository interface for managing inventory."""

    @abstractmethod
    def get_all(self) -> list[InventoryItem]: ...

    @abstractmethod
    def get_by_id(self, id: UUID) -> InventoryItem | None: ...

    @abstractmethod
    def get_by_name(self, name: str) -> InventoryItem | None: ...

    @abstractmethod
    def save(self, inventory_item: InventoryItem) -> None: ...

    @abstractmethod
    def delete(self, id: UUID) -> None: ...
