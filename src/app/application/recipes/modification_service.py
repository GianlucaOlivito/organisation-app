import logging
from uuid import UUID

from app.domain.recipes.recipe import Recipe

from .repository import RecipeRepository

logger = logging.getLogger(__name__)


class RecipeModificationService:
    """Service for use case UC-1.1: Create, Modify and Delete Recipe."""

    def __init__(self, recipe_repository: RecipeRepository) -> None:
        logger.debug("Initialized %s.", self.__class__.__name__)
        self._recipe_repository = recipe_repository

    def create(self, recipe: Recipe) -> Recipe:
        if self._recipe_repository.get_by_id(recipe.id):
            logger.warning("Failed to create existing recipe with ID '%s'.", recipe.id)
            raise ValueError(
                f"INVALID ARGUMENT: Recipe with ID '{recipe.id}' already exists."
            )
        self._recipe_repository.save(recipe)
        logger.info("Created recipe with ID '%s'.", recipe.id)
        return recipe

    def modify(self, recipe: Recipe) -> None:
        if not self._recipe_repository.get_by_id(recipe.id):
            logger.warning(
                "Failed to modify non-existent recipe with ID '%s'.", recipe.id
            )
            raise ValueError(
                f"INVALID ARGUMENT: Recipe with ID '{recipe.id}' does not exist."
            )
        self._recipe_repository.save(recipe)
        logger.info("Modified recipe with ID '%s'.", recipe.id)

    def delete(self, id: UUID) -> None:
        if not self._recipe_repository.get_by_id(id):
            logger.warning("Failed to delete non-existent recipe with ID '%s'.", id)
            raise ValueError(f"INVALID ARGUMENT: Recipe with ID '{id}' does not exist.")
        self._recipe_repository.delete(id)
        logger.info("Deleted recipe with ID '%s'.", id)
