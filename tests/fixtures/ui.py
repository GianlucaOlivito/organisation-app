import pytest

from app.adapters.inventory.markdown_shopping_list_exporter import (
    MarkdownShoppingListExporter,
)
from app.adapters.ui.components.inventory.inventory_filter_handler import (
    InventoryFilterHandler,
)
from app.adapters.ui.components.inventory.inventory_form import InventoryForm
from app.adapters.ui.components.inventory.shopping_list_filter_handler import (
    ShoppingListFilterHandler,
)
from app.adapters.ui.components.meal_planning.menu_filter_handler import (
    MenuFilterHandler,
)
from app.adapters.ui.components.meal_planning.menu_form import MenuForm
from app.adapters.ui.components.recipes.recipe_filter_handler import RecipeFilterHandler
from app.adapters.ui.components.recipes.recipe_form import RecipeForm
from app.adapters.ui.views.info_view import InfoView
from app.adapters.ui.views.inventory_view import InventoryView
from app.adapters.ui.views.logs_view import LogsView
from app.adapters.ui.views.menus_view import MenusView
from app.adapters.ui.views.recipes_view import RecipesView
from app.adapters.ui.views.shopping_list_view import ShoppingListView
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
from app.config.settings import settings
from app.domain.inventory.inventory_item import InventoryItem
from app.domain.meal_planning.menu import Menu
from app.domain.recipes.recipe import Recipe
from app.infrastructure.log_buffer import LogBuffer


class UpdateSpy:
    def __init__(self, side_effect=None):
        self.called = False
        self.call_count = 0
        self.call_args = None
        self.call_kwargs = None
        self.side_effect = side_effect

    def __call__(self, *args, **kwargs):
        self.called = True
        self.call_count += 1
        self.call_args = args
        self.call_kwargs = kwargs
        if self.side_effect:
            return self.side_effect(*args, **kwargs)

    def assert_called_once(self):
        assert self.called is True
        assert self.call_count == 1

    def assert_not_called(self):
        assert self.called is False

    def assert_called_once_with(self, *expected_args, **expected_kwargs):
        self.assert_called_once()
        assert self.call_args == expected_args
        assert self.call_kwargs == expected_kwargs


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
def shopping_list_filter_handler(
    inventory_shopping_list_service: ShoppingListService,
) -> ShoppingListFilterHandler:
    return ShoppingListFilterHandler(
        shopping_list_service=inventory_shopping_list_service
    )


@pytest.fixture
def recipe_form() -> RecipeForm:
    form = RecipeForm()
    form.update = UpdateSpy()
    return form


@pytest.fixture
def menu_form() -> MenuForm:
    form = MenuForm()
    form.update = UpdateSpy()
    return form


@pytest.fixture
def inventory_form() -> InventoryForm:
    form = InventoryForm()
    form.update = UpdateSpy()
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
    view.update = UpdateSpy()
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
    view.update = UpdateSpy()
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
    view.update = UpdateSpy()
    return view


@pytest.fixture
def shopping_list_view(
    inventory_shopping_list_service: ShoppingListService,
    inventory_reconciliation_service: InventoryReconciliationService,
    markdown_exporter: MarkdownShoppingListExporter,
) -> ShoppingListView:
    view = ShoppingListView(
        settings=settings,
        shopping_list_service=inventory_shopping_list_service,
        inventory_reconciliation_service=inventory_reconciliation_service,
        markdown_shopping_list_exporter=markdown_exporter,
    )
    view.update = UpdateSpy()
    return view


@pytest.fixture
def info_view() -> InfoView:
    view = InfoView(settings=settings)
    view.update = UpdateSpy()
    return view
