from datetime import date
from uuid import uuid4

import pytest

from app.application.inventory.modification_service import InventoryModificationService
from app.application.inventory.reconciliation_service import (
    InventoryReconciliationService,
)
from app.application.inventory.search_service import InventorySearchService
from app.application.meal_planning.search_service import MenuSearchService
from app.application.recipes.search_service import RecipeSearchService
from app.domain.inventory.inventory_item import InventoryItem
from app.domain.inventory.shopping_list import ShoppingList
from app.domain.inventory.shopping_list_item import ShoppingListItem
from app.domain.meal_planning.course import Course
from app.domain.meal_planning.menu import Menu
from app.domain.recipes.recipe import Recipe
from app.domain.recipes.recipe_ingredient import RecipeIngredient


@pytest.fixture
def inventory_search_service(fake_inventory_repo) -> InventorySearchService:
    return InventorySearchService(inventory_repository=fake_inventory_repo)


@pytest.fixture
def inventory_modification_service(
    fake_inventory_repo,
) -> InventoryModificationService:
    return InventoryModificationService(inventory_repository=fake_inventory_repo)


@pytest.fixture
def menu_search_service(fake_menu_repo) -> MenuSearchService:
    return MenuSearchService(menu_repository=fake_menu_repo)


@pytest.fixture
def recipe_search_service(fake_recipe_repo) -> RecipeSearchService:
    return RecipeSearchService(recipe_repository=fake_recipe_repo)


@pytest.fixture
def reconciliation_service(
    inventory_search_service,
    inventory_modification_service,
    menu_search_service,
    recipe_search_service,
) -> InventoryReconciliationService:
    return InventoryReconciliationService(
        inventory_search_service=inventory_search_service,
        inventory_modification_service=inventory_modification_service,
        menu_search_service=menu_search_service,
        recipe_search_service=recipe_search_service,
    )


def test_apply_shopping_list_updates_existing_and_creates_new_items(
    reconciliation_service, fake_inventory_repo
):
    existing_item = InventoryItem(id=uuid4(), name="Milk", quantity=1.0, unit="l")
    fake_inventory_repo.save(existing_item)

    shopping_list = ShoppingList(
        items=[
            ShoppingListItem(name="Milk", quantity=2.0, unit="l"),
            ShoppingListItem(name="Bread", quantity=1.0, unit="pcs"),
        ]
    )

    reconciliation_service.apply_shopping_list(shopping_list)

    inventory_items = fake_inventory_repo.get_all()
    assert len(inventory_items) == 2

    milk = next(item for item in inventory_items if item.name == "Milk")
    bread = next(item for item in inventory_items if item.name == "Bread")

    assert milk.id == existing_item.id
    assert milk.quantity == 3.0
    assert bread.quantity == 1.0


def test_consume_meals_for_period_raises_error_for_invalid_date_range(
    reconciliation_service,
):
    with pytest.raises(
        ValueError, match="INVALID ARGUMENT: Start date cannot be after end date."
    ):
        reconciliation_service.consume_meals_for_period(
            date(2026, 9, 10), date(2026, 9, 1)
        )


def test_consume_meals_for_period_deducts_stock_flooring_at_zero(
    reconciliation_service, fake_inventory_repo, fake_menu_repo, fake_recipe_repo
):
    cheese_item = InventoryItem(id=uuid4(), name="Cheese", quantity=100.0, unit="g")
    fake_inventory_repo.save(cheese_item)

    recipe = Recipe(
        id=uuid4(),
        name="Fondue",
        ingredients=[RecipeIngredient(name="Cheese", quantity=150.0, unit="g")],
    )
    fake_recipe_repo.save(recipe)

    menu = Menu(
        description="Dinner",
        scheduled_date=date(2026, 9, 1),
        courses=[Course(recipe_id=recipe.id, portions=1)],
    )
    fake_menu_repo.save(menu)

    reconciliation_service.consume_meals_for_period(date(2026, 9, 1), date(2026, 9, 2))

    saved_cheese = fake_inventory_repo.get_by_id(cheese_item.id)
    assert saved_cheese is not None
    assert saved_cheese.quantity == 0.0


def test_consume_meals_for_period_skips_missing_recipes(
    reconciliation_service, fake_inventory_repo, fake_menu_repo
):
    menu = Menu(
        description="Dinner",
        scheduled_date=date(2026, 9, 1),
        courses=[Course(recipe_id=uuid4(), portions=1)],
    )
    fake_menu_repo.save(menu)

    reconciliation_service.consume_meals_for_period(date(2026, 9, 1), date(2026, 9, 2))

    assert fake_inventory_repo.get_all() == []


def test_consume_meals_ignores_ingredients_not_present_in_inventory(
    reconciliation_service, fake_menu_repo, fake_recipe_repo, fake_inventory_repo
):
    recipe = Recipe(
        id=uuid4(),
        name="Tea",
        ingredients=[RecipeIngredient(name="Tea Bag", quantity=1.0, unit="pcs")],
    )
    fake_recipe_repo.save(recipe)
    fake_menu_repo.save(
        Menu(
            description="Tea Time",
            scheduled_date=date(2026, 9, 1),
            courses=[Course(recipe_id=recipe.id, portions=1)],
        )
    )

    reconciliation_service.consume_meals_for_period(date(2026, 9, 1), date(2026, 9, 2))

    assert fake_inventory_repo.get_all() == []
