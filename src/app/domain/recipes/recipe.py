from dataclasses import dataclass, field
from uuid import UUID, uuid4

from .recipe_ingredient import RecipeIngredient


@dataclass(kw_only=True, slots=True)
class Recipe:
    """Represents a recipe with its ingredients and unique identifier."""

    id: UUID = field(default_factory=uuid4)
    name: str
    ingredients: list[RecipeIngredient]
    instructions: str

    def __post_init__(self) -> None:
        if not (self.name or "").strip():
            raise ValueError("Ungültiger Rezeptname")
        if not self.ingredients:
            raise ValueError("Ungültige Zutatenliste")
        if not (self.instructions or "").strip():
            raise ValueError("Ungültige Zubereitung")
        self.name = self.name.strip()
        self.instructions = self.instructions.strip()
