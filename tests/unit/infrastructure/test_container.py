from app.adapters.inventory.markdown_shopping_list_exporter import (
    MarkdownShoppingListExporter,
)
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
from app.config.settings import Settings
from app.infrastructure.container import Container, create_container


def test_create_container_default_settings():
    container = create_container()

    assert isinstance(container, Container)
    assert isinstance(container.settings, Settings)
    assert isinstance(
        container.markdown_shopping_list_exporter, MarkdownShoppingListExporter
    )
    assert isinstance(
        container.inventory_modification_service, InventoryModificationService
    )
    assert isinstance(
        container.inventory_reconciliation_service,
        InventoryReconciliationService,
    )
    assert isinstance(container.inventory_search_service, InventorySearchService)
    assert isinstance(container.shopping_list_service, ShoppingListService)
    assert isinstance(container.menu_modification_service, MenuModificationService)
    assert isinstance(container.menu_search_service, MenuSearchService)
    assert isinstance(container.recipe_modification_service, RecipeModificationService)
    assert isinstance(container.recipe_search_service, RecipeSearchService)


def test_create_container_custom_settings(tmp_path):
    custom_settings = Settings(
        recipes_file_path=tmp_path / "test_recipes.json",
        menus_file_path=tmp_path / "test_menus.json",
        inventory_file_path=tmp_path / "test_inventory.json",
        shopping_list_file_path=tmp_path / "test_shopping_list.md",
    )
    container = create_container(app_settings=custom_settings)

    assert container.settings == custom_settings
    assert (
        container.inventory_search_service._inventory_repository._file_path  # type: ignore[attr-defined]
        == custom_settings.inventory_file_path
    )
    assert (
        container.menu_search_service._menu_repository._file_path  # type: ignore[attr-defined]
        == custom_settings.menus_file_path
    )
    assert (
        container.recipe_search_service._recipe_repository._file_path  # type: ignore[attr-defined]
        == custom_settings.recipes_file_path
    )
