from datetime import date
from uuid import uuid4

import pytest

from app.domain.inventory.inventory_item import InventoryItem
from app.domain.inventory.shopping_list import ShoppingList
from app.domain.inventory.shopping_list_item import ShoppingListItem
from app.domain.meal_planning.course import Course
from app.domain.meal_planning.menu import Menu
from app.domain.recipes.recipe import Recipe
from app.domain.recipes.recipe_ingredient import RecipeIngredient


def test_apply_shopping_list_updates_existing_and_creates_new_items(
    inventory_reconciliation_service, fake_inventory_repo
):
    existing_item = InventoryItem(name="Milk", quantity=1.0, unit="l")
    fake_inventory_repo.save(existing_item)
    shopping_list = ShoppingList(
        items=[
            ShoppingListItem(name="Milk", quantity=2.0, unit="l"),
            ShoppingListItem(name="Bread", quantity=1.0, unit="pcs"),
        ]
    )
    inventory_reconciliation_service.apply_shopping_list(shopping_list)
    inventory_items = fake_inventory_repo.get_all()

    assert len(inventory_items) == 2

    milk = next(item for item in inventory_items if item.name == "Milk")
    bread = next(item for item in inventory_items if item.name == "Bread")

    assert milk.id == existing_item.id
    assert milk.quantity == 3000
    assert milk.unit == "ml"
    assert bread.quantity == 1.0
    assert bread.unit == "pcs"


def test_consume_meals_for_period_raises_error_for_invalid_date_range(
    inventory_reconciliation_service,
):
    with pytest.raises(
        ValueError, match="INVALID ARGUMENT: Start date cannot be after end date."
    ):
        inventory_reconciliation_service.consume_meals_for_period(
            date(2026, 9, 10), date(2026, 9, 1)
        )


def test_consume_meals_for_period_deducts_stock_flooring_at_zero(
    inventory_reconciliation_service,
    fake_inventory_repo,
    fake_menu_repo,
    fake_recipe_repo,
):
    cheese_item = InventoryItem(name="Cheese", quantity=100.0, unit="g")
    fake_inventory_repo.save(cheese_item)
    recipe = Recipe(
        name="Fondue",
        ingredients=[RecipeIngredient(name="Cheese", quantity=150.0, unit="g")],
        instructions="Melt and enjoy.",
    )
    fake_recipe_repo.save(recipe)
    menu = Menu(
        description="Dinner",
        scheduled_date=date(2026, 9, 1),
        courses=[Course(recipe_id=recipe.id, portions=1)],
    )
    fake_menu_repo.save(menu)
    inventory_reconciliation_service.consume_meals_for_period(
        date(2026, 9, 1), date(2026, 9, 2)
    )
    saved_cheese = fake_inventory_repo.get_by_id(cheese_item.id)

    assert saved_cheese is not None
    assert saved_cheese.quantity == 0.0


def test_consume_meals_for_period_skips_missing_recipes(
    inventory_reconciliation_service, fake_inventory_repo, fake_menu_repo
):
    menu = Menu(
        description="Dinner",
        scheduled_date=date(2026, 9, 1),
        courses=[Course(recipe_id=uuid4(), portions=1)],
    )
    fake_menu_repo.save(menu)
    inventory_reconciliation_service.consume_meals_for_period(
        date(2026, 9, 1), date(2026, 9, 2)
    )

    assert fake_inventory_repo.get_all() == []


def test_consume_meals_ignores_ingredients_not_present_in_inventory(
    inventory_reconciliation_service,
    fake_menu_repo,
    fake_recipe_repo,
    fake_inventory_repo,
):
    recipe = Recipe(
        name="Tea",
        ingredients=[RecipeIngredient(name="Tea Bag", quantity=1.0, unit="pcs")],
        instructions="Boil and let cool down.",
    )
    fake_recipe_repo.save(recipe)
    fake_menu_repo.save(
        Menu(
            description="Tea Time",
            scheduled_date=date(2026, 9, 1),
            courses=[Course(recipe_id=recipe.id, portions=1)],
        )
    )
    inventory_reconciliation_service.consume_meals_for_period(
        date(2026, 9, 1), date(2026, 9, 2)
    )

    assert fake_inventory_repo.get_all() == []


def test_consume_meals_for_period_does_nothing_when_no_menus_exist(
    inventory_reconciliation_service, fake_inventory_repo
):
    item = InventoryItem(name="Milk", quantity=1000.0, unit="ml")
    fake_inventory_repo.save(item)
    inventory_reconciliation_service.consume_meals_for_period(
        date(2026, 9, 1), date(2026, 9, 2)
    )
    saved_item = fake_inventory_repo.get_by_id(item.id)

    assert saved_item.quantity == 1000.0


def test_consume_meals_for_period_handles_partial_stock(
    inventory_reconciliation_service,
    fake_inventory_repo,
    fake_menu_repo,
    fake_recipe_repo,
):
    fake_inventory_repo.save(InventoryItem(name="Sugar", quantity=50.0, unit="g"))
    recipe = Recipe(
        name="Cake",
        ingredients=[
            RecipeIngredient(name="Sugar", quantity=100.0, unit="g"),
            RecipeIngredient(name="Flour", quantity=200.0, unit="g"),
        ],
        instructions="Mix and bake.",
    )
    fake_recipe_repo.save(recipe)
    fake_menu_repo.save(
        Menu(
            description="Baking",
            scheduled_date=date(2026, 9, 1),
            courses=[Course(recipe_id=recipe.id, portions=1)],
        )
    )
    inventory_reconciliation_service.consume_meals_for_period(
        date(2026, 9, 1), date(2026, 9, 2)
    )
    sugar = next(item for item in fake_inventory_repo.get_all() if item.name == "Sugar")

    assert sugar.quantity == 0.0
