from uuid import UUID, uuid4

import flet as ft
import pytest

from app.adapters.ui.components.recipes.recipe_card import RecipeCard
from app.domain.recipes.recipe import Recipe
from app.domain.recipes.recipe_ingredient import RecipeIngredient


@pytest.fixture
def sample_recipe() -> Recipe:
    return Recipe(
        id=uuid4(),
        name="Spaghetti Carbonara",
        ingredients=[
            RecipeIngredient(name="Spaghetti", quantity=200.0, unit="g"),
            RecipeIngredient(name="Eier", quantity=2.0, unit=""),
            RecipeIngredient(name="Pecorino", quantity=50.5, unit="g"),
        ],
        instructions="Nudeln kochen. Eier und Käse verquirlen und unterheben.",
    )


def test_format_ingredient_quantities_and_units():
    ing_whole = RecipeIngredient(name="Eier", quantity=2.0, unit="")
    ing_unit = RecipeIngredient(name="Mehl", quantity=500.0, unit="g")
    ing_decimal = RecipeIngredient(name="Milch", quantity=1.5, unit="l")

    assert RecipeCard._format_ingredient(ing_whole) == "• 2 Eier"
    assert RecipeCard._format_ingredient(ing_unit) == "• 500 g Mehl"
    assert RecipeCard._format_ingredient(ing_decimal) == "• 1.5 l Milch"


def test_recipe_card_renders_full_data(sample_recipe):
    card = RecipeCard(sample_recipe)

    assert isinstance(card, ft.Card)

    column = card.content.content

    assert isinstance(column, ft.Column)

    header_row = column.controls[0]

    assert header_row.controls[0].value == "Spaghetti Carbonara"
    assert (
        header_row.controls[1].controls[0].value == f"ID: {str(sample_recipe.id)[:8]}"
    )

    ing_section = column.controls[2]

    assert ing_section.controls[0].value == "Zutaten"
    assert len(ing_section.controls) == 4
    assert ing_section.controls[1].value == "• 200 g Spaghetti"
    assert ing_section.controls[2].value == "• 2 Eier"
    assert ing_section.controls[3].value == "• 50.5 g Pecorino"

    inst_section = column.controls[4]

    assert inst_section.controls[0].value == "Zubereitung"
    assert (
        inst_section.controls[1].value
        == "Nudeln kochen. Eier und Käse verquirlen und unterheben."
    )


def test_recipe_card_callback_triggers(sample_recipe):
    edited_recipe = None
    deleted_id = None

    def on_edit(r: Recipe) -> None:
        nonlocal edited_recipe
        edited_recipe = r

    def on_delete(rid: UUID) -> None:
        nonlocal deleted_id
        deleted_id = rid

    card = RecipeCard(sample_recipe, on_edit=on_edit, on_delete=on_delete)
    header_row = card.content.content.controls[0]
    action_row = header_row.controls[1]
    edit_btn = action_row.controls[1]
    delete_btn = action_row.controls[2]
    edit_btn.on_click(None)

    assert edited_recipe == sample_recipe

    delete_btn.on_click(None)

    assert deleted_id == sample_recipe.id
