import logging
from collections import defaultdict

from app.application.recipes.search_service import RecipeSearchService
from app.domain.meal_planning.menu import Menu

logger = logging.getLogger(__name__)

UNIT_CONVERSIONS: dict[str, tuple[float, str]] = {
    # Mass -> Base: "g"
    "g": (1.0, "g"),
    "gramm": (1.0, "g"),
    "kg": (1000.0, "g"),
    "kilogramm": (1000.0, "g"),
    # Volume -> Base: "ml"
    "ml": (1.0, "ml"),
    "milliliter": (1.0, "ml"),
    "cl": (10.0, "ml"),
    "dl": (100.0, "ml"),
    "deziliter": (100.0, "ml"),
    "l": (1000.0, "ml"),
    "liter": (1000.0, "ml"),
    # Approximated culinary volume -> Base: "ml"
    "tl": (5.0, "ml"),
    "teelöffel": (5.0, "ml"),
    "el": (15.0, "ml"),
    "esslöffel": (15.0, "ml"),
    "prise": (0.5, "ml"),
    # Unitless aliases -> Base: ""
    "": (1.0, ""),
    "stk": (1.0, ""),
    "stück": (1.0, ""),
}


def standardize_unit(quantity: float, unit: str) -> tuple[float, str]:
    clean_unit = unit.strip().lower().rstrip(".")
    if clean_unit in UNIT_CONVERSIONS:
        factor, base_unit = UNIT_CONVERSIONS[clean_unit]
        return quantity * factor, base_unit
    return quantity, clean_unit


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
                    "Found no recipe with ID '%s' referenced in menu '%s'.",
                    course.recipe_id,
                    menu.id,
                )
                continue
            for ingredient in recipe.ingredients:
                std_qty, std_unit = standardize_unit(
                    ingredient.quantity, ingredient.unit
                )
                key = (ingredient.name, std_unit)
                totals[key] += std_qty * course.portions
    return totals
