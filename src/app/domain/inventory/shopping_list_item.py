from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class ShoppingListItem:
    """Represents an item on a shopping list."""

    name: str
    quantity: float
    unit: str

    def __post_init__(self) -> None:
        if self.quantity <= 0:
            raise ValueError("INVALID ARGUMENT: Item quantity must be positive.")
        if not self.name.strip():
            raise ValueError("INVALID ARGUMENT: Item name cannot be empty.")
