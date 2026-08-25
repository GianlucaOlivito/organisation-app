from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class RecipeIngredient:
    """Represents an ingredient reference within a Recipe."""

    name: str
    quantity: float
    unit: str

    def __post_init__(self) -> None:
        if self.quantity <= 0:
            raise ValueError("INVALID ARGUMENT: Ingredient quantity must be positive.")
        if not self.name.strip():
            raise ValueError("INVALID ARGUMENT: Ingredient name cannot be empty.")
