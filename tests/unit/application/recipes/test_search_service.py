from uuid import uuid4

import pytest

from app.application.recipes.search_service import RecipeSearchService
from app.domain.recipes.recipe import Recipe
from app.domain.recipes.recipe_ingredient import RecipeIngredient


@pytest.fixture
def search_service(fake_recipe_repo) -> RecipeSearchService:
    return RecipeSearchService(recipe_repository=fake_recipe_repo)


@pytest.fixture
def sample_recipes(fake_recipe_repo) -> list[Recipe]:
    recipe1 = Recipe(
        id=uuid4(),
        name="Spaghetti Carbonara",
        ingredients=[
            RecipeIngredient(name="Pasta", quantity=200.0, unit="g"),
            RecipeIngredient(name="Eggs", quantity=2.0, unit=""),
            RecipeIngredient(name="Guanciale", quantity=100.0, unit="g"),
        ],
    )
    recipe2 = Recipe(
        id=uuid4(),
        name="Tomato Soup",
        ingredients=[
            RecipeIngredient(name="Tomato", quantity=500.0, unit="g"),
            RecipeIngredient(name="Garlic", quantity=2.0, unit="cloves"),
        ],
    )
    fake_recipe_repo.save(recipe1)
    fake_recipe_repo.save(recipe2)
    return [recipe1, recipe2]


def test_get_all_returns_empty_list_when_no_recipes(search_service):
    assert search_service.get_all() == []


def test_get_all_returns_all_recipes(search_service, sample_recipes):
    results = search_service.get_all()
    assert len(results) == 2
    assert results == sample_recipes


def test_get_by_id_returns_recipe_when_found(search_service, sample_recipes):
    expected_recipe = sample_recipes[0]
    found_recipe = search_service.get_by_id(expected_recipe.id)
    assert found_recipe == expected_recipe


def test_get_by_id_returns_none_when_not_found(search_service):
    assert search_service.get_by_id(uuid4()) is None


def test_get_by_name_returns_recipe_when_found(search_service, sample_recipes):
    expected_recipe = sample_recipes[0]
    found_recipe = search_service.get_by_name("Spaghetti Carbonara")
    assert found_recipe == expected_recipe


def test_get_by_name_returns_none_when_not_found(search_service):
    assert search_service.get_by_name("Nonexistent Recipe") is None


def test_filter_by_ingredients_returns_matching_recipes(search_service, sample_recipes):
    results = search_service.filter_by_ingredients(["Pasta", "Eggs"])
    assert len(results) == 1
    assert results[0] == sample_recipes[0]


def test_filter_by_ingredients_returns_empty_list_when_no_match(
    search_service, sample_recipes
):
    results = search_service.filter_by_ingredients(["Chocolate"])
    assert results == []
