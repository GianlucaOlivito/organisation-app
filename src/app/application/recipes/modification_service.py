import logging
from uuid import UUID

from app.domain.recipes.recipe import Recipe

from .repository import RecipeRepository

logger = logging.getLogger(__name__)


class RecipeModificationService:
    """Service for use case UC-1.1: Create, Modify and Delete Recipe."""

    def __init__(self, recipe_repository: RecipeRepository) -> None:
        logger.debug("RecipeModificationService initialized.")
        self._recipe_repository = recipe_repository

    def create(self, recipe: Recipe) -> Recipe:
        if self._recipe_repository.get_by_id(recipe.id):
            logger.warning(f"Recipe creation failed: {recipe.name} already exists.")
            raise ValueError(
                f"INVALID ARGUMENT: Recipe '{recipe.name}' already exists."
            )
        self._recipe_repository.save(recipe)
        logger.info(f"Recipe created: {recipe.name}")
        return recipe

    def modify(self, recipe: Recipe) -> None:
        if not self._recipe_repository.get_by_id(recipe.id):
            logger.warning(f"Recipe modification failed: {recipe.name} does not exist.")
            raise ValueError(
                f"INVALID ARGUMENT: Recipe '{recipe.name}' does not exist."
            )
        self._recipe_repository.save(recipe)
        logger.info(f"Recipe modified: {recipe.name}")

    def delete(self, id: UUID) -> None:
        if not self._recipe_repository.get_by_id(id):
            logger.warning(
                f"Recipe deletion failed: Recipe with ID '{id}' does not exist."
            )
            raise ValueError(f"INVALID ARGUMENT: Recipe with ID '{id}' does not exist.")
        self._recipe_repository.delete(id)
        logger.info(f"Recipe with ID '{id}' deleted.")
