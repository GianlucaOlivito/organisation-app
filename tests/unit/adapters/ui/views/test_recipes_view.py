from unittest.mock import MagicMock

import flet as ft

from app.adapters.ui.components.recipes.recipe_card import RecipeCard
from app.adapters.ui.components.recipes.recipe_form import RecipeForm


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
    toolbar = recipes_view._toolbar

    assert isinstance(toolbar, ft.Row)
    assert len(toolbar.controls) == 5
    assert toolbar.controls[0] == recipes_view._add_button
    assert toolbar.controls[1] == recipes_view._search_button
    assert toolbar.controls[2] == recipes_view._search_input
    assert toolbar.controls[3] == recipes_view._filter_button
    assert toolbar.controls[4] == recipes_view._ingredient_input


def test_open_form_for_creation(recipes_view):
    recipes_view._open_form()

    assert recipes_view._toolbar.visible is False
    assert len(recipes_view._content_container.controls) == 1

    form = recipes_view._content_container.controls[0]

    assert isinstance(form, RecipeForm)
    assert form._recipe_id is not None


def test_open_form_for_editing(recipes_view, sample_recipes):
    recipe_to_edit = sample_recipes[0]
    recipes_view._open_form(recipe_to_edit)

    assert recipes_view._toolbar.visible is False
    assert len(recipes_view._content_container.controls) == 1

    form = recipes_view._content_container.controls[0]

    assert isinstance(form, RecipeForm)
    assert form._recipe_id == recipe_to_edit.id


def test_close_form_restores_toolbar(recipes_view):
    recipes_view._open_form()
    recipes_view._close_form()

    assert recipes_view._toolbar.visible is True


def test_save_form_creates_and_modifies_recipe(
    recipes_view, recipes_modification_service, sample_recipes
):
    recipes_modification_service.create = MagicMock()
    recipes_modification_service.modify = MagicMock()
    recipes_view._open_form()
    form = recipes_view._content_container.controls[0]
    form._on_save(sample_recipes[0])

    recipes_modification_service.create.assert_called_once_with(sample_recipes[0])

    recipes_view._open_form(sample_recipes[1])
    form = recipes_view._content_container.controls[0]
    form._on_save(sample_recipes[1])

    recipes_modification_service.modify.assert_called_once_with(sample_recipes[1])


def test_delete_recipe(recipes_view, sample_recipes):
    recipe_to_delete = sample_recipes[0]
    initial_count = len(recipes_view._grid.controls)
    recipes_view._delete_recipe(recipe_to_delete.id)

    assert len(recipes_view._grid.controls) == initial_count - 1
    assert all(
        card.recipe.id != recipe_to_delete.id for card in recipes_view._grid.controls
    )


def test_refresh_triggers_search(recipes_view):
    recipes_view._search_input.value = "Tomato Soup"
    recipes_view.refresh()

    assert len(recipes_view._grid.controls) == 1
    assert recipes_view._grid.controls[0].recipe.name == "Tomato Soup"
