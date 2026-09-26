from datetime import date
from unittest.mock import MagicMock
from uuid import uuid4

from app.application.common.calculators import calculate_menu_ingredients
from app.domain.meal_planning.course import Course
from app.domain.meal_planning.menu import Menu
from app.domain.recipes.recipe import Recipe
from app.domain.recipes.recipe_ingredient import RecipeIngredient


def test_calculate_menu_ingredients_aggregates_quantities_correctly():
    recipe_1 = Recipe(
        name="Pasta",
        ingredients=[
            RecipeIngredient(name="Pasta", quantity=100.0, unit="g"),
            RecipeIngredient(name="Tomato Sauce", quantity=50.0, unit="g"),
        ],
        instructions="Boil and enjoy.",
    )
    recipe_2 = Recipe(
        name="Salad",
        ingredients=[RecipeIngredient(name="Tomato Sauce", quantity=20.0, unit="g")],
        instructions="Mix and boil.",
    )
    recipe_search_service = MagicMock()
    recipe_search_service.get_by_id.side_effect = lambda r_id: {
        recipe_1.id: recipe_1,
        recipe_2.id: recipe_2,
    }.get(r_id)
    menus = [
        Menu(
            scheduled_date=date(2026, 1, 1),
            description="Dinner",
            courses=[
                Course(recipe_id=recipe_1.id, portions=2),  # Pasta: 200g, Sauce: 100g
                Course(recipe_id=recipe_2.id, portions=1),  # Sauce: 20g
            ],
        )
    ]
    totals = calculate_menu_ingredients(menus, recipe_search_service)

    assert totals[("Pasta", "g")] == 200.0
    assert totals[("Tomato Sauce", "g")] == 120.0


def test_calculate_menu_ingredients_handles_missing_recipes_gracefully():
    recipe_search_service = MagicMock()
    recipe_search_service.get_by_id.return_value = None
    menus = [
        Menu(
            scheduled_date=date(2026, 1, 1),
            description="Lunch",
            courses=[Course(recipe_id=uuid4(), portions=2)],
        )
    ]
    totals = calculate_menu_ingredients(menus, recipe_search_service)

    assert totals == {}


def test_calculate_menu_ingredients_returns_empty_dict_for_empty_menus():
    recipe_search_service = MagicMock()
    totals = calculate_menu_ingredients([], recipe_search_service)

    assert totals == {}
