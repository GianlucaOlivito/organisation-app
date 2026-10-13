import flet as ft

from app.domain.recipes.recipe import Recipe
from tests.fixtures.ui import UpdateSpy


def test_initialization_creation_mode(recipe_form):
    assert recipe_form._recipe_id is not None
    assert recipe_form._name_field.value == ""
    assert recipe_form._instructions_field.value == ""
    assert len(recipe_form._ingredients_column.controls) == 1


def test_initialization_edit_mode(sample_recipes, recipe_form):
    recipe_to_edit = sample_recipes[0]
    recipe_form.__init__(recipe=recipe_to_edit)
    recipe_form.update = UpdateSpy()

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
    delete_button.on_click(UpdateSpy())

    assert len(recipe_form._ingredients_column.controls) == 1


def test_extract_entity_constructs_valid_domain_model(recipe_form):
    recipe_form._name_field.value = " Tomato Soup "
    recipe_form._instructions_field.value = " Cook tomatoes. "
    row = recipe_form._ingredients_column.controls[0]
    row.controls[0].value = " Tomatoes "
    row.controls[1].value = " 4 "
    row.controls[2].value = " pcs "
    recipe = recipe_form._extract_entity()

    assert isinstance(recipe, Recipe)
    assert recipe.id == recipe_form._recipe_id
    assert recipe.name == "Tomato Soup"
    assert recipe.instructions == "Cook tomatoes."
    assert len(recipe.ingredients) == 1
    assert recipe.ingredients[0].name == "Tomatoes"
    assert recipe.ingredients[0].quantity == 4.0
    assert recipe.ingredients[0].unit == "pcs"


def test_extract_entity_filters_out_completely_empty_rows(recipe_form):
    recipe_form._name_field.value = "Pancakes"
    recipe_form._instructions_field.value = "Mix and fry."
    row1 = recipe_form._ingredients_column.controls[0]
    row1.controls[0].value = "Flour"
    row1.controls[1].value = "200"
    row1.controls[2].value = "g"
    recipe_form._add_ingredient_row("", "", "")
    recipe = recipe_form._extract_entity()

    assert len(recipe.ingredients) == 1
    assert recipe.ingredients[0].name == "Flour"
    assert recipe.ingredients[0].quantity == 200.0


def test_handle_save_success(recipe_form):
    on_save = UpdateSpy()
    recipe_form._on_save = on_save
    recipe_form._name_field.value = "Omelette"
    recipe_form._instructions_field.value = "Fry eggs in a pan."
    row = recipe_form._ingredients_column.controls[0]
    row.controls[0].value = "Eggs"
    row.controls[1].value = "2"
    row.controls[2].value = "pcs"
    recipe_form._handle_save(UpdateSpy())

    assert recipe_form._error_text.visible is False
    on_save.assert_called_once()

    saved_recipe = on_save.call_args[0]

    assert saved_recipe.name == "Omelette"


def test_handle_save_displays_error_on_validation_failure(recipe_form):
    on_save = UpdateSpy()
    recipe_form._on_save = on_save
    recipe_form._extract_entity = lambda: (_ for _ in ()).throw(
        ValueError("Name cannot be empty")
    )
    recipe_form._handle_save(UpdateSpy())

    assert recipe_form._error_text.visible is True
    assert recipe_form._error_text.value == "Name cannot be empty"
    on_save.assert_not_called()
    recipe_form.update.assert_called_once()


def test_close_button_triggers_on_close_callback(recipe_form):
    on_close = UpdateSpy()
    recipe_form._on_close = on_close
    header_row = recipe_form.controls[0]
    header_action_row = header_row.controls[1]
    close_button = header_action_row.controls[-1]
    close_button.on_click(UpdateSpy())

    on_close.assert_called_once()
