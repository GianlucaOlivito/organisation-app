import logging
from uuid import UUID

from app.domain.recipes.recipe import Recipe

from .repository import RecipeRepository

logger = logging.getLogger(__name__)


class RecipeSearchService:
    """Service for use case UC-1.2: Search and Filter Recipes."""

    def __init__(self, recipe_repository: RecipeRepository) -> None:
        self._recipe_repository = recipe_repository
        logger.debug("RecipeSearchService initialized.")

    def get_all(self) -> list[Recipe]:
        logger.debug("Fetched all available recipes.")
        return self._recipe_repository.get_all()

    def get_by_id(self, id: UUID) -> Recipe | None:
        logger.debug(f"Fetched recipe with ID {id}.")
        return self._recipe_repository.get_by_id(id)

    def get_by_name(self, name: str) -> Recipe | None:
        logger.debug(f"Fetched recipe with name {name}.")
        return self._recipe_repository.get_by_name(name)

    def filter_by_ingredients(self, ingredients: list[str]) -> list[Recipe]:
        logger.debug(f"Filtered recipes containing these ingredients: {ingredients}")
        return self._recipe_repository.filter_by_ingredients(ingredients)
