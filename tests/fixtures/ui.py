from unittest.mock import MagicMock

import pytest

from app.adapters.ui.components.inventory.inventory_filter_handler import (
    InventoryFilterHandler,
)
from app.adapters.ui.components.inventory.inventory_form import InventoryForm
from app.adapters.ui.components.meal_planning.menu_filter_handler import (
    MenuFilterHandler,
)
from app.adapters.ui.components.meal_planning.menu_form import MenuForm
from app.adapters.ui.components.recipes.recipe_filter_handler import RecipeFilterHandler
from app.adapters.ui.components.recipes.recipe_form import RecipeForm
from app.adapters.ui.views.inventory_view import InventoryView
from app.adapters.ui.views.logs_view import LogsView
from app.adapters.ui.views.menus_view import MenusView
from app.adapters.ui.views.recipes_view import RecipesView
from app.application.inventory.modification_service import InventoryModificationService
from app.application.inventory.search_service import InventorySearchService
from app.application.meal_planning.modification_service import MenuModificationService
from app.application.meal_planning.search_service import MenuSearchService
from app.application.recipes.modification_service import RecipeModificationService
from app.application.recipes.search_service import RecipeSearchService
from app.domain.inventory.inventory_item import InventoryItem
from app.domain.meal_planning.menu import Menu
from app.domain.recipes.recipe import Recipe
from app.infrastructure.log_buffer import LogBuffer


@pytest.fixture
def populated_recipe_search_service(
    recipes_search_service: RecipeSearchService,
    sample_recipes: list[Recipe],
) -> RecipeSearchService:
    for recipe in sample_recipes:
        recipes_search_service._recipe_repository.save(recipe)
    return recipes_search_service


@pytest.fixture
def populated_menu_search_service(
    meal_planning_search_service: MenuSearchService,
    sample_menus: list[Menu],
) -> MenuSearchService:
    for menu in sample_menus:
        meal_planning_search_service._menu_repository.save(menu)
    return meal_planning_search_service


@pytest.fixture
def populated_inventory_search_service(
    inventory_search_service: InventorySearchService,
    sample_items: list[InventoryItem],
) -> InventorySearchService:
    for item in sample_items:
        inventory_search_service._inventory_repository.save(item)
    return inventory_search_service


@pytest.fixture
def recipe_filter_handler(
    populated_recipe_search_service: RecipeSearchService,
) -> RecipeFilterHandler:
    return RecipeFilterHandler(search_service=populated_recipe_search_service)


@pytest.fixture
def menu_filter_handler(
    populated_menu_search_service: MenuSearchService,
) -> MenuFilterHandler:
    return MenuFilterHandler(search_service=populated_menu_search_service)


@pytest.fixture
def inventory_filter_handler(
    populated_inventory_search_service: InventorySearchService,
) -> InventoryFilterHandler:
    return InventoryFilterHandler(search_service=populated_inventory_search_service)


@pytest.fixture
def recipe_form() -> RecipeForm:
    form = RecipeForm()
    form.update = MagicMock()
    return form


@pytest.fixture
def menu_form() -> MenuForm:
    form = MenuForm()
    form.update = MagicMock()
    return form


@pytest.fixture
def inventory_form() -> InventoryForm:
    form = InventoryForm()
    form.update = MagicMock()
    return form


@pytest.fixture
def logs_view(log_buffer: LogBuffer) -> LogsView:
    return LogsView(log_buffer=log_buffer)


@pytest.fixture
def recipes_view(
    recipes_modification_service: RecipeModificationService,
    populated_recipe_search_service: RecipeSearchService,
) -> RecipesView:
    view = RecipesView(
        modification_service=recipes_modification_service,
        search_service=populated_recipe_search_service,
    )
    view.update = MagicMock()
    return view


@pytest.fixture
def menus_view(
    meal_planning_modification_service: MenuModificationService,
    populated_menu_search_service: MenuSearchService,
    populated_recipe_search_service: RecipeSearchService,
) -> MenusView:
    view = MenusView(
        modification_service=meal_planning_modification_service,
        menu_search_service=populated_menu_search_service,
        recipe_search_service=populated_recipe_search_service,
    )
    view.update = MagicMock()
    return view


@pytest.fixture
def inventory_view(
    inventory_modification_service: InventoryModificationService,
    populated_inventory_search_service: InventorySearchService,
) -> InventoryView:
    view = InventoryView(
        modification_service=inventory_modification_service,
        search_service=populated_inventory_search_service,
    )
    view.update = MagicMock()
    return view
