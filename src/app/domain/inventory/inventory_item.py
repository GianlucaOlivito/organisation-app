from dataclasses import dataclass, field
from uuid import UUID, uuid4


@dataclass(kw_only=True, slots=True)
class InventoryItem:
    """Represents a tracked ingredient or supply item in stock."""

    id: UUID = field(default_factory=uuid4)
    name: str
    quantity: float
    unit: str

    def __post_init__(self) -> None:
        if self.quantity < 0:
            raise ValueError("INVALID ARGUMENT: Item quantity cannot be negative.")
        if not self.name.strip():
            raise ValueError("INVALID ARGUMENT: Item name cannot be empty.")
