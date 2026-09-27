import math
from dataclasses import dataclass, field
from uuid import UUID, uuid4


@dataclass(kw_only=True, slots=True)
class InventoryItem:
    """Represents a tracked ingredient or supply item in stock."""

    id: UUID = field(default_factory=uuid4)
    name: str
    quantity: float | str
    unit: str

    def __post_init__(self) -> None:
        if not (self.name or "").strip():
            raise ValueError("Ungültiger Name")
        try:
            raw_qty = str(self.quantity).replace(",", ".")
            qty = float(raw_qty)
        except TypeError, ValueError:
            raise ValueError("Ungültige Menge")
        if math.isnan(qty) or math.isinf(qty) or qty < 0:
            raise ValueError("Ungültige Menge")
        self.name = self.name.strip()
        self.quantity = qty
        self.unit = (self.unit or "").strip()
