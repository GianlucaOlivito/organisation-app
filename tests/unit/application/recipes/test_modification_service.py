from dataclasses import replace
from uuid import uuid4

import pytest

from app.domain.recipes.recipe import Recipe


def test_create_recipe_success(
    recipes_modification_service, fake_recipe_repo, sample_ingredient
):
    recipe = Recipe(
        name="Pancakes", ingredients=[sample_ingredient], instructions="Mix and fry."
    )
    created_recipe = recipes_modification_service.create(recipe)

    assert created_recipe == recipe
    assert fake_recipe_repo.get_by_id(recipe.id) == recipe


def test_create_recipe_already_exists_raises_error(
    recipes_modification_service, sample_recipes
):
    sample_recipe = sample_recipes[0]

    with pytest.raises(
        ValueError,
        match=f"INVALID ARGUMENT: Recipe with ID '{sample_recipe.id}' already exists.",
    ):
        recipes_modification_service.create(sample_recipe)


def test_modify_recipe_success(
    recipes_modification_service, fake_recipe_repo, sample_recipes
):
    sample_recipe = sample_recipes[0]
    updated_recipe = replace(sample_recipe, name="Spaghetti Carbonara Extra Cheese")
    recipes_modification_service.modify(updated_recipe)
    saved_recipe = fake_recipe_repo.get_by_id(sample_recipe.id)

    assert saved_recipe.name == "Spaghetti Carbonara Extra Cheese"


def test_modify_recipe_not_found_raises_error(
    recipes_modification_service, sample_ingredient
):
    unregistered_recipe = Recipe(
        name="Unsaved Dish",
        ingredients=[sample_ingredient],
        instructions="Mix and fry.",
    )

    with pytest.raises(
        ValueError,
        match=f"INVALID ARGUMENT: Recipe with ID '{unregistered_recipe.id}' does not exist.",
    ):
        recipes_modification_service.modify(unregistered_recipe)


def test_delete_recipe_success(
    recipes_modification_service, fake_recipe_repo, sample_recipes
):
    sample_recipe = sample_recipes[0]
    recipes_modification_service.delete(sample_recipe.id)

    assert fake_recipe_repo.get_by_id(sample_recipe.id) is None


def test_delete_recipe_not_found_raises_error(recipes_modification_service):
    random_id = uuid4()

    with pytest.raises(
        ValueError, match=f"Recipe with ID '{random_id}' does not exist"
    ):
        recipes_modification_service.delete(random_id)
