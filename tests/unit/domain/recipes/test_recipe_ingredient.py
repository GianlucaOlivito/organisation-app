from dataclasses import FrozenInstanceError

import pytest

from app.domain.recipes.recipe_ingredient import RecipeIngredient


def test_create_valid_recipe_ingredient():
    ingredient = RecipeIngredient(name="Flour", quantity=500.0, unit="g")

    assert ingredient.name == "Flour"
    assert ingredient.quantity == 500.0
    assert ingredient.unit == "g"


@pytest.mark.parametrize("invalid_quantity", [0.0, -10.0])
def test_recipe_ingredient_raises_error_for_non_positive_quantity(invalid_quantity):
    with pytest.raises(
        ValueError, match="INVALID ARGUMENT: Ingredient quantity must be positive."
    ):
        RecipeIngredient(name="Sugar", quantity=invalid_quantity, unit="g")


@pytest.mark.parametrize("invalid_name", ["", "   "])
def test_recipe_ingredient_raises_error_for_empty_name(invalid_name):
    with pytest.raises(
        ValueError, match="INVALID ARGUMENT: Ingredient name cannot be empty."
    ):
        RecipeIngredient(name=invalid_name, quantity=100.0, unit="g")


def test_recipe_ingredient_is_immutable():
    ingredient = RecipeIngredient(name="Salt", quantity=5.0, unit="g")

    with pytest.raises(FrozenInstanceError):
        ingredient.quantity = 10.0  # type: ignore[misc]
