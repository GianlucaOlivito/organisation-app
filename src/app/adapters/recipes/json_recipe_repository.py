import logging
from pathlib import Path
from typing import Any
from uuid import UUID

from app.adapters.common.json_file_handler import read_json_file, write_json_file
from app.application.recipes.repository import RecipeRepository
from app.config.settings import settings
from app.domain.recipes.recipe import Recipe
from app.domain.recipes.recipe_ingredient import RecipeIngredient

logger = logging.getLogger(__name__)


class JsonRecipeRepository(RecipeRepository):
    """Implementation part of UC-1.1 and UC-1.2: Manage recipes persistence with JSON."""

    def __init__(self, file_path: Path | None = None) -> None:
        self._file_path = file_path or settings.recipes_file_path
        logger.debug("JsonRecipeRepository initialized with path: %s", self._file_path)

    def _recipe_to_dict(self, recipe: Recipe) -> dict[str, Any]:
        return {
            "id": str(recipe.id),
            "name": recipe.name,
            "ingredients": [
                {
                    "name": ing.name,
                    "quantity": ing.quantity,
                    "unit": ing.unit,
                }
                for ing in recipe.ingredients
            ],
            "instructions": recipe.instructions,
        }

    def _dict_to_recipe(self, data: dict[str, Any]) -> Recipe:
        ingredients = [
            RecipeIngredient(
                name=ing_data["name"],
                quantity=float(ing_data["quantity"]),
                unit=ing_data["unit"],
            )
            for ing_data in data.get("ingredients", [])
        ]
        return Recipe(
            id=UUID(data["id"]),
            name=data["name"],
            ingredients=ingredients,
            instructions=data.get("instructions", ""),
        )

    def get_all(self) -> list[Recipe]:
        raw_data = read_json_file(self._file_path)
        recipes: list[Recipe] = []
        for item in raw_data:
            try:
                recipes.append(self._dict_to_recipe(item))
            except (KeyError, ValueError, TypeError) as e:
                logger.error("Skipping invalid recipe entry: %s. Error: %s", item, e)
        logger.debug("Retrieved %d recipes from %s.", len(recipes), self._file_path)
        return recipes

    def get_by_id(self, id: UUID) -> Recipe | None:
        recipe = next((r for r in self.get_all() if r.id == id), None)
        if recipe:
            logger.debug("Found recipe with ID '%s'.", id)
        else:
            logger.debug("No recipe found with ID '%s'.", id)
        return recipe

    def get_by_name(self, name: str) -> Recipe | None:
        normalized_name = name.strip().lower()
        recipe = next(
            (r for r in self.get_all() if r.name.strip().lower() == normalized_name),
            None,
        )
        if recipe:
            logger.debug("Found recipe with name '%s'.", name)
        else:
            logger.debug("No recipe found with name '%s'.", name)
        return recipe

    def filter_by_ingredients(self, ingredients: list[str]) -> list[Recipe]:
        if not ingredients:
            return self.get_all()
        target_ingredients = {ing.strip().lower() for ing in ingredients if ing.strip()}
        matching_recipes: list[Recipe] = []
        for recipe in self.get_all():
            recipe_ingredient_names = {
                ing.name.strip().lower() for ing in recipe.ingredients
            }
            if target_ingredients.issubset(recipe_ingredient_names):
                matching_recipes.append(recipe)
        logger.debug(
            "Filtered recipes by ingredients %s. Found %d matching recipes.",
            target_ingredients,
            len(matching_recipes),
        )
        return matching_recipes

    def save(self, recipe: Recipe) -> None:
        recipes = self.get_all()
        updated = False
        for idx, existing in enumerate(recipes):
            if existing.id == recipe.id:
                recipes[idx] = recipe
                updated = True
                break
        if not updated:
            recipes.append(recipe)
        serialized = [self._recipe_to_dict(r) for r in recipes]
        write_json_file(self._file_path, serialized)
        logger.info(
            "Saved recipe '%s' (ID: %s) to '%s'.",
            recipe.name,
            recipe.id,
            self._file_path,
        )

    def delete(self, id: UUID) -> None:
        recipes = self.get_all()
        filtered = [r for r in recipes if r.id != id]
        if len(filtered) != len(recipes):
            serialized = [self._recipe_to_dict(r) for r in filtered]
            write_json_file(self._file_path, serialized)
            logger.info("Deleted recipe with ID '%s' from '%s'.", id, self._file_path)
        else:
            logger.warning("Attempted to delete non-existent recipe with ID '%s'.", id)
