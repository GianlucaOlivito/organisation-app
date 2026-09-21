import logging
from pathlib import Path
from typing import Any
from uuid import UUID

from app.adapters.common.json_base_repository import JsonBaseRepository
from app.application.recipes.repository import RecipeRepository
from app.config.settings import settings
from app.domain.recipes.recipe import Recipe
from app.domain.recipes.recipe_ingredient import RecipeIngredient

logger = logging.getLogger(__name__)


class JsonRecipeRepository(JsonBaseRepository[Recipe], RecipeRepository):
    """Implementation part of UC-1.1 and UC-1.2: Manage recipes persistence with JSON."""

    def __init__(self, file_path: Path | None = None) -> None:
        super().__init__(file_path=file_path or settings.recipes_file_path)

    def _entity_to_dict(self, recipe: Recipe) -> dict[str, Any]:
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

    def _dict_to_entity(self, data: dict[str, Any]) -> Recipe:
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

    def get_by_name(self, name: str) -> Recipe | None:
        normalized_name = name.strip().lower()
        recipe = next(
            (r for r in self.get_all() if r.name.strip().lower() == normalized_name),
            None,
        )
        if recipe:
            logger.debug("Found entity with name '%s'.", name)
        else:
            logger.debug("Failed to find entity with name '%s'.", name)
        return recipe

    def filter_by_ingredients(self, ingredients: list[str]) -> list[Recipe]:
        target_ingredients = {ing.strip().lower() for ing in ingredients if ing.strip()}
        if not target_ingredients:
            return self.get_all()
        matching_recipes: list[Recipe] = []
        for recipe in self.get_all():
            recipe_ingredient_names = {
                ing.name.strip().lower() for ing in recipe.ingredients
            }
            if target_ingredients.issubset(recipe_ingredient_names):
                matching_recipes.append(recipe)
        ingredients_str = ", ".join(sorted(target_ingredients))
        logger.debug(
            "Found %d recipes matching ingredients '%s'.",
            len(matching_recipes),
            ingredients_str,
        )
        return matching_recipes
