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
