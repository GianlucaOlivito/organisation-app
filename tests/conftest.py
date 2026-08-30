import pytest

from tests.fakes.fake_menu_repository import FakeMenuRepository
from tests.fakes.fake_recipe_repository import FakeRecipeRepository


@pytest.fixture
def fake_recipe_repo() -> FakeRecipeRepository:
    """Provides a fresh in-memory repository for tests."""

    return FakeRecipeRepository()


@pytest.fixture
def fake_menu_repo() -> FakeMenuRepository:
    """Provides a fresh in-memory repository for tests."""

    return FakeMenuRepository()
