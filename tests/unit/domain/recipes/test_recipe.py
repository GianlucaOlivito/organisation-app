from uuid import UUID

from app.domain.recipes.recipe import Recipe
from app.domain.recipes.recipe_ingredient import RecipeIngredient


def test_create_recipe_with_defaults():
    recipe = Recipe(name="Pancakes")

    assert isinstance(recipe.id, UUID)
    assert recipe.name == "Pancakes"
    assert recipe.ingredients == []
    assert recipe.instructions == ""


def test_create_recipe_with_custom_attributes():
    ingredient = RecipeIngredient(name="Milk", quantity=250.0, unit="ml")
    recipe = Recipe(
        name="Pancakes", ingredients=[ingredient], instructions="Mix and fry."
    )

    assert recipe.name == "Pancakes"
    assert len(recipe.ingredients) == 1
    assert recipe.ingredients[0] == ingredient
    assert recipe.instructions == "Mix and fry."


def test_recipe_instances_have_unique_uuids_and_isolated_lists():
    recipe_1 = Recipe(name="Recipe 1")
    recipe_2 = Recipe(name="Recipe 2")

    assert recipe_1.id != recipe_2.id

    ingredient = RecipeIngredient(name="Egg", quantity=2.0, unit="pcs")
    recipe_1.ingredients.append(ingredient)

    assert len(recipe_1.ingredients) == 1
    assert len(recipe_2.ingredients) == 0
