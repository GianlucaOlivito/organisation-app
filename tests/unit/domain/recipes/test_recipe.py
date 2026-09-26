from uuid import UUID

import pytest

from app.domain.recipes.recipe import Recipe
from app.domain.recipes.recipe_ingredient import RecipeIngredient


def test_create_valid_recipe(sample_ingredient):
    recipe = Recipe(
        name="Pancakes", ingredients=[sample_ingredient], instructions="Mix and fry."
    )

    assert isinstance(recipe.id, UUID)
    assert recipe.name == "Pancakes"
    assert recipe.ingredients[0] == sample_ingredient
    assert recipe.instructions == "Mix and fry."


def test_recipe_instances_have_unique_uuids_and_isolated_lists(sample_ingredient):
    recipe_1 = Recipe(
        name="Recipe 1", ingredients=[sample_ingredient], instructions="Mix and fry."
    )
    recipe_2 = Recipe(
        name="Recipe 2", ingredients=[sample_ingredient], instructions="Mix and fry."
    )

    assert recipe_1.id != recipe_2.id

    ingredient = RecipeIngredient(name="Egg", quantity=2.0, unit="pcs")
    recipe_1.ingredients.append(ingredient)

    assert len(recipe_1.ingredients) == 2
    assert len(recipe_2.ingredients) == 1


def test_recipe_strips_whitespace_from_fields(sample_ingredient):
    recipe = Recipe(
        name="  Pancakes  ",
        ingredients=[sample_ingredient],
        instructions="  Mix and fry.  ",
    )

    assert recipe.name == "Pancakes"
    assert recipe.instructions == "Mix and fry."


@pytest.mark.parametrize("invalid_name", ["", "   "])
def test_recipe_raises_error_for_empty_name(sample_ingredient, invalid_name):
    with pytest.raises(ValueError, match="Ungültiger Rezeptname"):
        Recipe(
            name=invalid_name,
            ingredients=[sample_ingredient],
            instructions="Mix and fry.",
        )


def test_recipe_raises_error_for_empty_ingredients():
    with pytest.raises(ValueError, match="Ungültige Zutatenliste"):
        Recipe(
            name="Pancakes",
            ingredients=[],
            instructions="Mix and fry.",
        )


@pytest.mark.parametrize("invalid_instructions", ["", "   "])
def test_recipe_raises_error_for_empty_instructions(
    sample_ingredient, invalid_instructions
):
    with pytest.raises(ValueError, match="Ungültige Zubereitung"):
        Recipe(
            name="Pancakes",
            ingredients=[sample_ingredient],
            instructions=invalid_instructions,
        )
