import flet as ft

from app.adapters.ui.components.recipes.recipe_card import RecipeCard
from app.domain.recipes.recipe_ingredient import RecipeIngredient


def test_format_ingredient_quantities_and_units():
    ing_whole = RecipeIngredient(name="Eier", quantity=2.0, unit="")
    ing_unit = RecipeIngredient(name="Mehl", quantity=500.0, unit="g")
    ing_decimal = RecipeIngredient(name="Milch", quantity=1.5, unit="l")

    assert RecipeCard._format_ingredient(ing_whole) == "• 2 Eier"
    assert RecipeCard._format_ingredient(ing_unit) == "• 500 g Mehl"
    assert RecipeCard._format_ingredient(ing_decimal) == "• 1.5 l Milch"


def test_recipe_card_renders_full_data(sample_recipes):
    recipe = sample_recipes[0]
    card = RecipeCard(recipe)

    assert isinstance(card, ft.Card)

    column = card.content.content

    assert isinstance(column, ft.Column)

    header_row = column.controls[0]

    assert header_row.controls[0].value == recipe.name
    assert header_row.controls[1].controls[0].value == f"ID: {str(recipe.id)[:8]}"

    ing_section = column.controls[2]

    assert ing_section.controls[0].value == "Zutaten"
    assert len(ing_section.controls) == len(recipe.ingredients) + 1
    for i, ingredient in enumerate(recipe.ingredients):
        assert ing_section.controls[i + 1].value == RecipeCard._format_ingredient(
            ingredient
        )

    inst_section = column.controls[4]

    assert inst_section.controls[0].value == "Zubereitung"
    assert inst_section.controls[1].value == recipe.instructions


def test_recipe_card_callback_triggers(sample_recipes):
    recipe = sample_recipes[0]
    edited_recipe = None
    deleted_id = None

    def on_edit(recipe) -> None:
        nonlocal edited_recipe
        edited_recipe = recipe

    def on_delete(recipe_id) -> None:
        nonlocal deleted_id
        deleted_id = recipe_id

    card = RecipeCard(recipe, on_edit=on_edit, on_delete=on_delete)
    header_row = card.content.content.controls[0]
    action_row = header_row.controls[1]
    edit_btn = action_row.controls[1]
    delete_btn = action_row.controls[2]
    edit_btn.on_click(None)

    assert edited_recipe == recipe

    delete_btn.on_click(None)

    assert deleted_id == recipe.id
