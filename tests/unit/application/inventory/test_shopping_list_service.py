from datetime import date
from uuid import uuid4

import pytest

from app.domain.inventory.inventory_item import InventoryItem
from app.domain.meal_planning.course import Course
from app.domain.meal_planning.menu import Menu
from app.domain.recipes.recipe import Recipe
from app.domain.recipes.recipe_ingredient import RecipeIngredient


def test_generate_shopping_list_raises_error_for_invalid_date_range(
    inventory_shopping_list_service,
):
    with pytest.raises(
        ValueError, match="INVALID ARGUMENT: Start date cannot be after end date."
    ):
        inventory_shopping_list_service.generate_shopping_list(
            date(2026, 9, 10), date(2026, 9, 1)
        )


def test_generate_shopping_list_calculates_needed_ingredients(
    inventory_shopping_list_service,
    fake_recipe_repo,
    fake_menu_repo,
    fake_inventory_repo,
):
    recipe = Recipe(
        name="Butter Chicken",
        ingredients=[RecipeIngredient(name="Butter", quantity=100.0, unit="g")],
        instructions="Bake in the oven.",
    )
    fake_recipe_repo.save(recipe)
    menu = Menu(
        description="Dinner",
        scheduled_date=date(2026, 9, 1),
        courses=[Course(recipe_id=recipe.id, portions=2)],
    )
    fake_menu_repo.save(menu)
    fake_inventory_repo.save(InventoryItem(name="Butter", quantity=50.0, unit="g"))
    result = inventory_shopping_list_service.generate_shopping_list(
        date(2026, 9, 1), date(2026, 9, 7)
    )

    assert len(result.items) == 1
    assert result.items[0].name == "Butter"
    assert result.items[0].quantity == 150.0
    assert result.items[0].unit == "g"


def test_generate_shopping_list_skips_missing_recipes(
    inventory_shopping_list_service, fake_menu_repo
):
    menu = Menu(
        description="Dinner",
        scheduled_date=date(2026, 9, 1),
        courses=[Course(recipe_id=uuid4(), portions=1)],
    )
    fake_menu_repo.save(menu)
    result = inventory_shopping_list_service.generate_shopping_list(
        date(2026, 9, 1), date(2026, 9, 7)
    )

    assert result.items == []


def test_generate_shopping_list_returns_empty_when_stock_is_sufficient(
    inventory_shopping_list_service,
    fake_recipe_repo,
    fake_menu_repo,
    fake_inventory_repo,
):
    recipe = Recipe(
        name="Oatmeal",
        ingredients=[RecipeIngredient(name="Oats", quantity=100.0, unit="g")],
        instructions="Meal and enjoy.",
    )
    fake_recipe_repo.save(recipe)
    fake_menu_repo.save(
        Menu(
            description="Breakfast",
            scheduled_date=date(2026, 9, 1),
            courses=[Course(recipe_id=recipe.id, portions=1)],
        )
    )
    fake_inventory_repo.save(InventoryItem(name="Oats", quantity=200.0, unit="g"))
    result = inventory_shopping_list_service.generate_shopping_list(
        date(2026, 9, 1), date(2026, 9, 2)
    )

    assert result.items == []


def test_generate_shopping_list_aggregates_same_ingredient_across_courses(
    inventory_shopping_list_service, fake_recipe_repo, fake_menu_repo
):
    recipe = Recipe(
        name="Omelette",
        ingredients=[RecipeIngredient(name="Egg", quantity=2.0, unit="pcs")],
        instructions="Mix and fry.",
    )
    fake_recipe_repo.save(recipe)
    fake_menu_repo.save(
        Menu(
            description="Brunch",
            scheduled_date=date(2026, 9, 1),
            courses=[
                Course(recipe_id=recipe.id, portions=1),
                Course(recipe_id=recipe.id, portions=2),
            ],
        )
    )
    result = inventory_shopping_list_service.generate_shopping_list(
        date(2026, 9, 1), date(2026, 9, 2)
    )

    assert len(result.items) == 1
    assert result.items[0].quantity == 6.0
