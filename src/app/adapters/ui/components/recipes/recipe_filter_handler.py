from app.adapters.ui.components.common.filter_helpers import parse_str_to_uuid
from app.application.recipes.search_service import RecipeSearchService
from app.domain.recipes.recipe import Recipe


class RecipeFilterHandler:
    """Encapsulates filter rules and search logic for recipes."""

    def __init__(self, search_service: RecipeSearchService) -> None:
        self._search_service = search_service

    def _filter_by_query(self, query: str) -> list[Recipe]:
        if parsed_id := parse_str_to_uuid(query):
            recipe_by_id = self._search_service.get_by_id(parsed_id)
            return [recipe_by_id] if recipe_by_id else []
        recipe_by_name = self._search_service.get_by_name(query)
        return [recipe_by_name] if recipe_by_name else []

    def filter(
        self,
        query: str | None = None,
        ing_query: str | None = None,
    ) -> list[Recipe]:
        clean_query = (query or "").strip()
        clean_ing_query = (ing_query or "").strip()
        if clean_query:
            return self._filter_by_query(clean_query)
        if clean_ing_query:
            ingredients = [i.strip() for i in clean_ing_query.split(",") if i.strip()]
            return self._search_service.filter_by_ingredients(ingredients)
        return self._search_service.get_all()
