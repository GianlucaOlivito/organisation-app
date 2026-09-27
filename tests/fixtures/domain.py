from datetime import date

import pytest

from app.domain.inventory.inventory_item import InventoryItem
from app.domain.meal_planning.course import Course
from app.domain.meal_planning.menu import Menu
from app.domain.recipes.recipe import Recipe
from app.domain.recipes.recipe_ingredient import RecipeIngredient
from tests.fakes.fake_inventory_repository import FakeInventoryRepository
from tests.fakes.fake_menu_repository import FakeMenuRepository
from tests.fakes.fake_recipe_repository import FakeRecipeRepository


def create_recipe(
    name: str = "Spaghetti Carbonara", ingredients: list[RecipeIngredient] | None = None
) -> Recipe:
    if ingredients is None:
        ingredients = [
            RecipeIngredient(name="Pasta", quantity=200.0, unit="g"),
            RecipeIngredient(name="Eggs", quantity=2.0, unit=""),
        ]
    return Recipe(name=name, ingredients=ingredients, instructions="Mix and fry.")


@pytest.fixture
def sample_ingredient() -> RecipeIngredient:
    return RecipeIngredient(name="Milk", quantity=250.0, unit="ml")


@pytest.fixture
def sample_recipes(fake_recipe_repo: FakeRecipeRepository) -> list[Recipe]:
    recipes = [
        create_recipe(name="Spaghetti Carbonara"),
        create_recipe(
            name="Tomato Soup",
            ingredients=[
                RecipeIngredient(name="Tomato", quantity=500.0, unit="g"),
                RecipeIngredient(name="Garlic", quantity=2.0, unit="cloves"),
            ],
        ),
    ]
    for recipe in recipes:
        fake_recipe_repo.save(recipe)
    return recipes


@pytest.fixture
def sample_menus(
    fake_menu_repo: FakeMenuRepository, sample_recipes: list[Recipe]
) -> list[Menu]:
    menus = [
        Menu(
            scheduled_date=date(2026, 9, 1),
            description="Lunch",
            courses=[Course(recipe_id=sample_recipes[0].id, portions=2)],
        ),
        Menu(
            scheduled_date=date(2026, 9, 10),
            description="Dinner",
            courses=[Course(recipe_id=sample_recipes[1].id, portions=2)],
        ),
    ]
    for menu in menus:
        fake_menu_repo.save(menu)
    return menus


@pytest.fixture
def sample_items(fake_inventory_repo: FakeInventoryRepository) -> list[InventoryItem]:
    items = [
        InventoryItem(name="Milk", quantity=2.0, unit="l"),
        InventoryItem(name="Eggs", quantity=12.0, unit=""),
    ]
    for item in items:
        fake_inventory_repo.save(item)
    return items
