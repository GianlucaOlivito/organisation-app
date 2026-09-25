from uuid import UUID

from app.application.recipes.search_service import RecipeSearchService
from app.domain.recipes.recipe import Recipe


class RecipeFilterHandler:
    """Encapsulates filter rules and search logic for recipes."""

    def __init__(self, search_service: RecipeSearchService) -> None:
        self._search_service = search_service

    def filter(
        self,
        query: str | None = None,
        ing_query: str | None = None,
    ) -> list[Recipe]:
        clean_query = (query or "").strip()
        clean_ing_query = (ing_query or "").strip()
        if not clean_query and not clean_ing_query:
            return self._search_service.get_all()
        if not clean_query and clean_ing_query:
            ingredients = [i.strip() for i in clean_ing_query.split(",") if i.strip()]
            return self._search_service.filter_by_ingredients(ingredients)
        recipes = self._filter_by_query(clean_query)
        if not clean_ing_query:
            return recipes
        return self._filter_by_ingredients_in_memory(recipes, clean_ing_query)

    def _filter_by_query(self, query: str) -> list[Recipe]:
        try:
            parsed_id = UUID(query)
            recipe_by_id = self._search_service.get_by_id(parsed_id)
            return [recipe_by_id] if recipe_by_id else []
        except ValueError:
            pass
        recipe_by_name = self._search_service.get_by_name(query)
        return [recipe_by_name] if recipe_by_name else []

    def _filter_by_ingredients_in_memory(
        self, recipes: list[Recipe], ingredient_query: str
    ) -> list[Recipe]:
        target_ings = {
            i.strip().lower() for i in ingredient_query.split(",") if i.strip()
        }
        if not target_ings:
            return recipes
        matching: list[Recipe] = []
        for recipe in recipes:
            recipe_ing_names = {ing.name.strip().lower() for ing in recipe.ingredients}
            if target_ings.issubset(recipe_ing_names):
                matching.append(recipe)
        return matching
