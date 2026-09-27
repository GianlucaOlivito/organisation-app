import pytest

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
