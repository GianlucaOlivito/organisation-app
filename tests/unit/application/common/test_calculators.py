from datetime import date
from unittest.mock import MagicMock
from uuid import uuid4

import pytest

from app.application.common.calculators import (
    calculate_menu_ingredients,
    standardize_unit,
)
from app.domain.meal_planning.course import Course
from app.domain.meal_planning.menu import Menu
from app.domain.recipes.recipe import Recipe
from app.domain.recipes.recipe_ingredient import RecipeIngredient


@pytest.mark.parametrize(
    "quantity, raw_unit, expected_qty, expected_unit",
    [
        (500.0, "g", 500.0, "g"),
        (200.0, "Gramm", 200.0, "g"),
        (1.5, "kg", 1500.0, "g"),
        (2.0, "Kilogramm", 2000.0, "g"),
        (1.0, "kg.", 1000.0, "g"),
        (250.0, "ml", 250.0, "ml"),
        (100.0, "Milliliter", 100.0, "ml"),
        (2.0, "cl", 20.0, "ml"),
        (5.0, "dl", 500.0, "ml"),
        (1.0, "Deziliter", 100.0, "ml"),
        (0.75, "l", 750.0, "ml"),
        (2.0, "Liter", 2000.0, "ml"),
        (1.0, "l.", 1000.0, "ml"),
        (2.0, "tl", 10.0, "ml"),
        (1.0, "Teelöffel", 5.0, "ml"),
        (3.0, "EL", 45.0, "ml"),
        (1.0, "Esslöffel", 15.0, "ml"),
        (2.0, "prise", 1.0, "ml"),
        (1.0, "el.", 15.0, "ml"),
        (5.0, "", 5.0, ""),
        (3.0, "stk", 3.0, ""),
        (4.0, "Stk.", 4.0, ""),
        (2.0, "Stück", 2.0, ""),
        (10.0, "Dose", 10.0, "dose"),
        (1.0, "Packung", 1.0, "packung"),
        (2.0, "Pck.", 2.0, "pck"),
    ],
)
def test_standardize_unit_converts_units_correctly(
    quantity: float, raw_unit: str, expected_qty: float, expected_unit: str
):
    qty, unit = standardize_unit(quantity, raw_unit)
    assert qty == expected_qty
    assert unit == expected_unit


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
                Course(recipe_id=recipe_1.id, portions=2),
                Course(recipe_id=recipe_2.id, portions=1),
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
