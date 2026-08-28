from abc import ABC, abstractmethod
from uuid import UUID

from app.domain.recipes.recipe import Recipe


class RecipeRepository(ABC):
    """Repository interface for managing recipes."""

    @abstractmethod
    def get_all(self) -> list[Recipe]: ...

    @abstractmethod
    def get_by_id(self, id: UUID) -> Recipe | None: ...

    @abstractmethod
    def get_by_name(self, name: str) -> Recipe | None: ...

    @abstractmethod
    def filter_by_ingredients(self, ingredients: list[str]) -> list[Recipe]: ...

    @abstractmethod
    def save(self, recipe: Recipe) -> None: ...

    @abstractmethod
    def delete(self, id: UUID) -> None: ...
