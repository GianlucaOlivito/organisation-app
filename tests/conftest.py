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


@pytest.fixture
def fake_recipe_repo() -> FakeRecipeRepository:
    return FakeRecipeRepository()


@pytest.fixture
def fake_menu_repo() -> FakeMenuRepository:
    return FakeMenuRepository()


@pytest.fixture
def fake_inventory_repo() -> FakeInventoryRepository:
    return FakeInventoryRepository()


@pytest.fixture
def sample_recipes(fake_recipe_repo: FakeRecipeRepository) -> list[Recipe]:
    recipe1 = Recipe(
        name="Spaghetti Carbonara",
        ingredients=[
            RecipeIngredient(name="Pasta", quantity=200.0, unit="g"),
            RecipeIngredient(name="Eggs", quantity=2.0, unit=""),
            RecipeIngredient(name="Guanciale", quantity=100.0, unit="g"),
        ],
    )
    recipe2 = Recipe(
        name="Tomato Soup",
        ingredients=[
            RecipeIngredient(name="Tomato", quantity=500.0, unit="g"),
            RecipeIngredient(name="Garlic", quantity=2.0, unit="cloves"),
        ],
    )
    fake_recipe_repo.save(recipe1)
    fake_recipe_repo.save(recipe2)
    return [recipe1, recipe2]


@pytest.fixture
def sample_menus(
    fake_menu_repo: FakeMenuRepository, sample_recipes: list[Recipe]
) -> list[Menu]:
    menu1 = Menu(
        scheduled_date=date(2026, 9, 1),
        description="Lunch",
        courses=[Course(recipe_id=sample_recipes[0].id, portions=2)],
    )
    menu2 = Menu(
        scheduled_date=date(2026, 9, 10),
        description="Dinner",
        courses=[Course(recipe_id=sample_recipes[1].id, portions=2)],
    )
    fake_menu_repo.save(menu1)
    fake_menu_repo.save(menu2)
    return [menu1, menu2]


@pytest.fixture
def sample_items(fake_inventory_repo: FakeInventoryRepository) -> list[InventoryItem]:
    item1 = InventoryItem(name="Milk", quantity=2.0, unit="l")
    item2 = InventoryItem(name="Eggs", quantity=12.0, unit="")
    fake_inventory_repo.save(item1)
    fake_inventory_repo.save(item2)
    return [item1, item2]
