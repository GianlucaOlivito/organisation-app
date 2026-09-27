from dataclasses import dataclass, field
from uuid import UUID, uuid4

from .shopping_list_item import ShoppingListItem


@dataclass(kw_only=True, slots=True)
class ShoppingList:
    """Represents a shopping list with a unique ID and a list of items."""

    id: UUID = field(default_factory=uuid4)
    items: list[ShoppingListItem] = field(default_factory=list)

    def __post_init__(self) -> None:
        if not self.items:
            raise ValueError("Ungültige Einkaufsliste")
