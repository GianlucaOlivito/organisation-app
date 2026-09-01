from abc import ABC, abstractmethod
from pathlib import Path

from app.domain.inventory.shopping_list import ShoppingList


class ShoppingListExporter(ABC):
    """
    Interface for use case UC-3.4: Export Shopping List.
    Will be implemented in the adapters layer.
    """

    @abstractmethod
    def export(self, shopping_list: ShoppingList, destination: Path) -> None: ...
