from pathlib import Path

import pytest

from app.adapters.inventory.json_inventory_repository import JsonInventoryRepository
from app.adapters.inventory.markdown_shopping_list_exporter import (
    MarkdownShoppingListExporter,
)
from app.adapters.meal_planning.json_menu_repository import JsonMenuRepository
from app.adapters.recipes.json_recipe_repository import JsonRecipeRepository


@pytest.fixture
def json_recipe_repo(tmp_path: Path) -> JsonRecipeRepository:
    file_path = tmp_path / "recipes.json"
    return JsonRecipeRepository(file_path=file_path)


@pytest.fixture
def json_menu_repo(tmp_path: Path) -> JsonMenuRepository:
    file_path = tmp_path / "menus.json"
    return JsonMenuRepository(file_path=file_path)


@pytest.fixture
def json_inventory_repo(tmp_path: Path) -> JsonInventoryRepository:
    file_path = tmp_path / "inventory.json"
    return JsonInventoryRepository(file_path=file_path)


@pytest.fixture
def markdown_exporter() -> MarkdownShoppingListExporter:
    return MarkdownShoppingListExporter()
