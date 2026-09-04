import logging
from collections import defaultdict

from app.application.recipes.search_service import RecipeSearchService
from app.domain.meal_planning.menu import Menu

logger = logging.getLogger(__name__)


def calculate_menu_ingredients(
    menus: list[Menu],
    recipe_search_service: RecipeSearchService,
) -> dict[tuple[str, str], float]:
    totals: dict[tuple[str, str], float] = defaultdict(float)

    for menu in menus:
        for course in menu.courses:
            recipe = recipe_search_service.get_by_id(course.recipe_id)
            if recipe is None:
                logger.warning(
                    f"Recipe with ID '{course.recipe_id}' referenced in menu '{menu.id}' not found."
                )
                continue
            for ingredient in recipe.ingredients:
                key = (ingredient.name, ingredient.unit)
                totals[key] += ingredient.quantity * course.portions
    return totals
