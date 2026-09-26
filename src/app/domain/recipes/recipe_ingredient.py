import math
from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class RecipeIngredient:
    """Represents an ingredient reference within a Recipe."""

    name: str
    quantity: float | str
    unit: str

    def __post_init__(self) -> None:
        if not (self.name or "").strip():
            raise ValueError("Ungültiger Zutatenname")
        try:
            raw_qty = str(self.quantity).replace(",", ".")
            qty = float(raw_qty)
        except TypeError, ValueError:
            raise ValueError("Ungültige Menge")
        if math.isnan(qty) or math.isinf(qty) or qty <= 0:
            raise ValueError("Ungültige Menge")
        object.__setattr__(self, "name", self.name.strip())
        object.__setattr__(self, "quantity", qty)
        object.__setattr__(self, "unit", (self.unit or "").strip())
