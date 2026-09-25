import flet as ft
import pytest

from app.adapters.ui.components.recipes.recipe_card import RecipeCard
from app.adapters.ui.views.recipes_view import RecipesView
from app.application.recipes.modification_service import RecipeModificationService
from app.application.recipes.search_service import RecipeSearchService
from app.domain.recipes.recipe import Recipe


@pytest.fixture
def recipes_view(
    recipes_modification_service: RecipeModificationService,
    recipes_search_service: RecipeSearchService,
    sample_recipes: list[Recipe],
) -> RecipesView:
    return RecipesView(
        modification_service=recipes_modification_service,
        search_service=recipes_search_service,
    )


def test_initialization_renders_sample_recipes(recipes_view, sample_recipes):
    assert len(recipes_view._grid.controls) == 2
    assert isinstance(recipes_view._grid.controls[0], RecipeCard)
    assert recipes_view._grid.controls[0].recipe == sample_recipes[0]


def test_search_by_name(recipes_view):
    recipes_view._search_input.value = "Tomato Soup"
    recipes_view._search()

    assert len(recipes_view._grid.controls) == 1
    assert recipes_view._grid.controls[0].recipe.name == "Tomato Soup"


def test_search_empty_state_when_no_match(recipes_view):
    recipes_view._search_input.value = "Non Existent Recipe"
    recipes_view._search()

    assert recipes_view._content_container.controls == [recipes_view._empty_state]


def test_filter_by_ingredient(recipes_view):
    recipes_view._ingredient_input.value = "Pasta"
    recipes_view._filter()

    assert len(recipes_view._grid.controls) == 1
    assert recipes_view._grid.controls[0].recipe.name == "Spaghetti Carbonara"


def test_search_and_filter_reset_opposite_channel(recipes_view):
    recipes_view._search_input.value = "Spaghetti Carbonara"
    recipes_view._ingredient_input.value = "Tomato"
    recipes_view._filter()

    assert len(recipes_view._grid.controls) == 1
    assert recipes_view._grid.controls[0].recipe.name == "Tomato Soup"


def test_toolbar_structure(recipes_view):
    toolbar = recipes_view.controls[2]

    assert isinstance(toolbar, ft.Row)
    assert len(toolbar.controls) == 4
    assert toolbar.controls[0] == recipes_view._search_button
    assert toolbar.controls[1] == recipes_view._search_input
    assert toolbar.controls[2] == recipes_view._filter_button
    assert toolbar.controls[3] == recipes_view._ingredient_input
