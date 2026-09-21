import logging
from dataclasses import dataclass

from app.adapters.inventory.json_inventory_repository import JsonInventoryRepository
from app.adapters.inventory.markdown_shopping_list_exporter import (
    MarkdownShoppingListExporter,
)
from app.adapters.meal_planning.json_menu_repository import JsonMenuRepository
from app.adapters.recipes.json_recipe_repository import JsonRecipeRepository
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
from app.config.settings import Settings, settings
from app.infrastructure.log_buffer import LogBuffer
from app.infrastructure.logging_setup import setup_logging

logger = logging.getLogger(__name__)


@dataclass(frozen=True, slots=True)
class Container:
    """Represents a container for dependency injection (composition root)."""

    settings: Settings
    log_buffer: LogBuffer
    markdown_shopping_list_exporter: MarkdownShoppingListExporter
    inventory_modification_service: InventoryModificationService
    inventory_reconciliation_service: InventoryReconciliationService
    inventory_search_service: InventorySearchService
    shopping_list_service: ShoppingListService
    menu_modification_service: MenuModificationService
    menu_search_service: MenuSearchService
    recipe_modification_service: RecipeModificationService
    recipe_search_service: RecipeSearchService


def create_container(app_settings: Settings = settings) -> Container:
    log_buffer = LogBuffer(app_settings.log_buffer_size)
    setup_logging(log_buffer)
    logger.info("Initializing application...")
    json_inventory_repo = JsonInventoryRepository(app_settings.inventory_file_path)
    json_menu_repo = JsonMenuRepository(app_settings.menus_file_path)
    json_recipe_repo = JsonRecipeRepository(app_settings.recipes_file_path)
    md_shopping_list_exporter = MarkdownShoppingListExporter()
    inventory_modification_service = InventoryModificationService(json_inventory_repo)
    inventory_search_service = InventorySearchService(json_inventory_repo)
    menu_modification_service = MenuModificationService(json_menu_repo)
    menu_search_service = MenuSearchService(json_menu_repo)
    recipe_modification_service = RecipeModificationService(json_recipe_repo)
    recipe_search_service = RecipeSearchService(json_recipe_repo)
    inventory_reconciliation_service = InventoryReconciliationService(
        inventory_search_service,
        inventory_modification_service,
        menu_search_service,
        recipe_search_service,
    )
    shopping_list_service = ShoppingListService(
        recipe_search_service,
        menu_search_service,
        inventory_search_service,
    )
    return Container(
        settings=app_settings,
        log_buffer=log_buffer,
        markdown_shopping_list_exporter=md_shopping_list_exporter,
        inventory_modification_service=inventory_modification_service,
        inventory_reconciliation_service=inventory_reconciliation_service,
        inventory_search_service=inventory_search_service,
        shopping_list_service=shopping_list_service,
        menu_modification_service=menu_modification_service,
        menu_search_service=menu_search_service,
        recipe_modification_service=recipe_modification_service,
        recipe_search_service=recipe_search_service,
    )
