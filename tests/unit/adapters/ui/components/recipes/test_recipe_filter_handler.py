import pytest

from app.adapters.ui.components.recipes.recipe_filter_handler import (
    RecipeFilterHandler,
)
from app.application.recipes.search_service import RecipeSearchService
from app.domain.recipes.recipe import Recipe


@pytest.fixture
def filter_handler(
    recipes_search_service: RecipeSearchService,
    sample_recipes: list[Recipe],
) -> RecipeFilterHandler:
    return RecipeFilterHandler(search_service=recipes_search_service)


def test_filter_returns_all_when_queries_are_empty(filter_handler, sample_recipes):
    results = filter_handler.filter(query="", ing_query="")

    assert len(results) == 2
    assert results == sample_recipes


def test_filter_by_recipe_name(filter_handler):
    results = filter_handler.filter(query="Spaghetti Carbonara")

    assert len(results) == 1
    assert results[0].name == "Spaghetti Carbonara"


def test_filter_by_recipe_id(filter_handler, sample_recipes):
    target_recipe = sample_recipes[0]
    results = filter_handler.filter(query=str(target_recipe.id))

    assert len(results) == 1
    assert results[0].id == target_recipe.id


def test_filter_by_ingredients_repository_search(filter_handler):
    results = filter_handler.filter(ing_query="Tomato")

    assert len(results) == 1
    assert results[0].name == "Tomato Soup"


def test_filter_by_query_and_ingredients_in_memory(filter_handler):
    matching = filter_handler.filter(
        query="Spaghetti Carbonara", ing_query="Pasta, Eggs"
    )

    assert len(matching) == 1
    assert matching[0].name == "Spaghetti Carbonara"

    mismatch = filter_handler.filter(query="Spaghetti Carbonara", ing_query="Tomato")

    assert len(mismatch) == 0


def test_filter_invalid_uuid_falls_back_to_name_search(filter_handler):
    results = filter_handler.filter(query="non-existent-recipe")

    assert len(results) == 0
