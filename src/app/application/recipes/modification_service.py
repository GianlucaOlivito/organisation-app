from uuid import UUID

from app.domain.recipes.recipe import Recipe

from .repository import RecipeRepository


class RecipeModificationService:
    """Service for use case UC-1.1: Create, Modify and Delete Recipe."""

    def __init__(self, recipe_repository: RecipeRepository) -> None:
        self._recipe_repository = recipe_repository

    def create(self, recipe: Recipe) -> Recipe:
        if self._recipe_repository.get_by_id(recipe.id):
            raise ValueError(
                f"INVALID ARGUMENT: Recipe '{recipe.name}' already exists."
            )
        self._recipe_repository.save(recipe)
        return recipe

    def modify(self, recipe: Recipe) -> None:
        if not self._recipe_repository.get_by_id(recipe.id):
            raise ValueError(
                f"INVALID ARGUMENT: Recipe '{recipe.name}' does not exist."
            )
        self._recipe_repository.save(recipe)

    def delete(self, id: UUID) -> None:
        if not self._recipe_repository.get_by_id(id):
            raise ValueError(f"INVALID ARGUMENT: Recipe with ID '{id}' does not exist.")
        self._recipe_repository.delete(id)
