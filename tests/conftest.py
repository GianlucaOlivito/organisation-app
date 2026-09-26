from datetime import date

import pytest

from app.application.inventory.modification_service import InventoryModificationService
from app.application.inventory.reconciliation_service import (
    InventoryReconciliationService,
)
from app.application.inventory.search_service import InventorySearchService
from app.application.inventory.shopping_list_service import ShoppingListService
from app.application.meal_planning.modification_service import MenuModificationService
from app.application.meal_planning.search_service import MenuSearchService
from app.application.recipes.modification_service import RecipeModificationService
from app.application.recipes.search_service import RecipeSearchService
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
def sample_ingredient() -> RecipeIngredient:
    return RecipeIngredient(name="Milk", quantity=250.0, unit="ml")


@pytest.fixture
def sample_recipes(fake_recipe_repo: FakeRecipeRepository) -> list[Recipe]:
    recipe1 = Recipe(
        name="Spaghetti Carbonara",
        ingredients=[
            RecipeIngredient(name="Pasta", quantity=200.0, unit="g"),
            RecipeIngredient(name="Eggs", quantity=2.0, unit=""),
            RecipeIngredient(name="Guanciale", quantity=100.0, unit="g"),
        ],
        instructions="Mix and fry.",
    )
    recipe2 = Recipe(
        name="Tomato Soup",
        ingredients=[
            RecipeIngredient(name="Tomato", quantity=500.0, unit="g"),
            RecipeIngredient(name="Garlic", quantity=2.0, unit="cloves"),
        ],
        instructions="Mix and fry.",
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


@pytest.fixture
def recipes_modification_service(fake_recipe_repo) -> RecipeModificationService:
    return RecipeModificationService(recipe_repository=fake_recipe_repo)


@pytest.fixture
def recipes_search_service(fake_recipe_repo) -> RecipeSearchService:
    return RecipeSearchService(recipe_repository=fake_recipe_repo)


@pytest.fixture
def meal_planning_modification_service(fake_menu_repo) -> MenuModificationService:
    return MenuModificationService(menu_repository=fake_menu_repo)


@pytest.fixture
def meal_planning_search_service(fake_menu_repo) -> MenuSearchService:
    return MenuSearchService(menu_repository=fake_menu_repo)


@pytest.fixture
def inventory_modification_service(fake_inventory_repo) -> InventoryModificationService:
    return InventoryModificationService(inventory_repository=fake_inventory_repo)


@pytest.fixture
def inventory_search_service(fake_inventory_repo) -> InventorySearchService:
    return InventorySearchService(inventory_repository=fake_inventory_repo)


@pytest.fixture
def inventory_reconciliation_service(
    inventory_search_service,
    inventory_modification_service,
    meal_planning_search_service,
    recipes_search_service,
) -> InventoryReconciliationService:
    return InventoryReconciliationService(
        inventory_search_service=inventory_search_service,
        inventory_modification_service=inventory_modification_service,
        menu_search_service=meal_planning_search_service,
        recipe_search_service=recipes_search_service,
    )


@pytest.fixture
def inventory_shopping_list_service(
    recipes_search_service, meal_planning_search_service, inventory_search_service
) -> ShoppingListService:
    return ShoppingListService(
        recipe_search_service=recipes_search_service,
        menu_search_service=meal_planning_search_service,
        inventory_search_service=inventory_search_service,
    )
