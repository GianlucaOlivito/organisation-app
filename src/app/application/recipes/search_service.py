from uuid import UUID

from app.domain.recipes.recipe import Recipe

from .repository import RecipeRepository


class RecipeSearchService:
    """Service for use case UC-1.2: Search and Filter Recipes."""

    def __init__(self, recipe_repository: RecipeRepository) -> None:
        self._recipe_repository = recipe_repository

    def get_all(self) -> list[Recipe]:
        return self._recipe_repository.get_all()

    def get_by_id(self, id: UUID) -> Recipe | None:
        return self._recipe_repository.get_by_id(id)

    def get_by_name(self, name: str) -> Recipe | None:
        return self._recipe_repository.get_by_name(name)

    def filter_by_ingredients(self, ingredients: list[str]) -> list[Recipe]:
        return self._recipe_repository.filter_by_ingredients(ingredients)
