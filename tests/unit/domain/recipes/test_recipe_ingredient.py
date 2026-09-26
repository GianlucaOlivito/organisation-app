import math
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
    with pytest.raises(ValueError, match="Ungültige Menge"):
        RecipeIngredient(name="Sugar", quantity=invalid_quantity, unit="g")


@pytest.mark.parametrize("invalid_name", ["", "   "])
def test_recipe_ingredient_raises_error_for_empty_name(invalid_name):
    with pytest.raises(ValueError, match="Ungültiger Zutatenname"):
        RecipeIngredient(name=invalid_name, quantity=100.0, unit="g")


@pytest.mark.parametrize("invalid_qty", ["abc", None, math.nan, math.inf])
def test_recipe_ingredient_raises_error_for_invalid_quantity_types(invalid_qty):
    with pytest.raises(ValueError, match="Ungültige Menge"):
        RecipeIngredient(name="Sugar", quantity=invalid_qty, unit="g")


def test_recipe_ingredient_parses_comma_and_string_quantity():
    ingredient = RecipeIngredient(name=" Flour ", quantity="1,5", unit=" kg ")

    assert ingredient.name == "Flour"
    assert ingredient.quantity == 1.5
    assert ingredient.unit == "kg"


def test_recipe_ingredient_is_immutable():
    ingredient = RecipeIngredient(name="Salt", quantity=5.0, unit="g")

    with pytest.raises(FrozenInstanceError):
        ingredient.quantity = 10.0  # type: ignore[misc]
