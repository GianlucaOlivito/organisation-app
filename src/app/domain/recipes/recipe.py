from dataclasses import dataclass, field
from uuid import UUID, uuid4

from .recipe_ingredient import RecipeIngredient


@dataclass(kw_only=True, slots=True)
class Recipe:
    """Represents a recipe with its ingredients and unique identifier."""

    id: UUID = field(default_factory=uuid4)
    name: str
    ingredients: list[RecipeIngredient] = field(default_factory=list)
    instructions: str = ""
