from unittest.mock import MagicMock

import flet as ft

from app.domain.recipes.recipe import Recipe


def test_initialization_creation_mode(recipe_form):
    assert recipe_form._recipe_id is not None
    assert recipe_form._name_field.value == ""
    assert recipe_form._instructions_field.value == ""
    assert len(recipe_form._ingredients_column.controls) == 1


def test_initialization_edit_mode(sample_recipes, recipe_form):
    recipe_to_edit = sample_recipes[0]
    recipe_form.__init__(recipe=recipe_to_edit)
    recipe_form.update = MagicMock()

    assert recipe_form._recipe_id == recipe_to_edit.id
    assert recipe_form._name_field.value == recipe_to_edit.name
    assert recipe_form._instructions_field.value == recipe_to_edit.instructions
    assert len(recipe_form._ingredients_column.controls) == len(
        recipe_to_edit.ingredients
    )

    first_row = recipe_form._ingredients_column.controls[0]

    assert first_row.controls[0].value == "Pasta"
    assert first_row.controls[1].value == "200.0"
    assert first_row.controls[2].value == "g"


def test_add_ingredient_row(recipe_form):
    initial_count = len(recipe_form._ingredients_column.controls)
    recipe_form._add_ingredient_row("Garlic", "2", "cloves")

    assert len(recipe_form._ingredients_column.controls) == initial_count + 1

    new_row = recipe_form._ingredients_column.controls[-1]

    assert isinstance(new_row, ft.Row)
    assert new_row.controls[0].value == "Garlic"
    assert new_row.controls[1].value == "2"
    assert new_row.controls[2].value == "cloves"


def test_delete_ingredient_row(recipe_form):
    recipe_form._add_ingredient_row("Salt", "1", "pinch")

    assert len(recipe_form._ingredients_column.controls) == 2

    delete_button = recipe_form._ingredients_column.controls[1].controls[3]
    delete_button.on_click(MagicMock())

    assert len(recipe_form._ingredients_column.controls) == 1


def test_get_recipe_constructs_valid_domain_model(recipe_form):
    recipe_form._name_field.value = " Tomato Soup "
    recipe_form._instructions_field.value = " Cook tomatoes. "
    row = recipe_form._ingredients_column.controls[0]
    row.controls[0].value = " Tomatoes "
    row.controls[1].value = " 4 "
    row.controls[2].value = " pcs "
    recipe = recipe_form.get_recipe()

    assert isinstance(recipe, Recipe)
    assert recipe.id == recipe_form._recipe_id
    assert recipe.name == "Tomato Soup"
    assert recipe.instructions == "Cook tomatoes."
    assert len(recipe.ingredients) == 1
    assert recipe.ingredients[0].name == "Tomatoes"
    assert recipe.ingredients[0].quantity == 4.0
    assert recipe.ingredients[0].unit == "pcs"


def test_get_recipe_filters_out_completely_empty_rows(recipe_form):
    recipe_form._name_field.value = "Pancakes"
    recipe_form._instructions_field.value = "Mix and fry."
    row1 = recipe_form._ingredients_column.controls[0]
    row1.controls[0].value = "Flour"
    row1.controls[1].value = "200"
    row1.controls[2].value = "g"
    recipe_form._add_ingredient_row("", "", "")
    recipe = recipe_form.get_recipe()

    assert len(recipe.ingredients) == 1
    assert recipe.ingredients[0].name == "Flour"
    assert recipe.ingredients[0].quantity == 200.0


def test_handle_save_success(recipe_form):
    on_save_mock = MagicMock()
    recipe_form._on_save = on_save_mock
    recipe_form._name_field.value = "Omelette"
    recipe_form._instructions_field.value = "Fry eggs in a pan."
    row = recipe_form._ingredients_column.controls[0]
    row.controls[0].value = "Eggs"
    row.controls[1].value = "2"
    row.controls[2].value = "pcs"
    mock_event = MagicMock()
    recipe_form._handle_save(mock_event)

    assert recipe_form._error_text.visible is False
    on_save_mock.assert_called_once()

    saved_recipe = on_save_mock.call_args[0][0]

    assert saved_recipe.name == "Omelette"


def test_handle_save_displays_error_on_validation_failure(recipe_form):
    on_save_mock = MagicMock()
    recipe_form._on_save = on_save_mock
    recipe_form.get_recipe = MagicMock(side_effect=ValueError("Name cannot be empty"))
    mock_event = MagicMock()
    recipe_form._handle_save(mock_event)

    assert recipe_form._error_text.visible is True
    assert recipe_form._error_text.value == "Name cannot be empty"
    on_save_mock.assert_not_called()
    recipe_form.update.assert_called_once()
