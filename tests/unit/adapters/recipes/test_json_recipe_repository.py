import json
import logging
from pathlib import Path
from uuid import UUID, uuid4

import pytest

from app.adapters.recipes.json_recipe_repository import JsonRecipeRepository
from app.domain.recipes.recipe import Recipe
from app.domain.recipes.recipe_ingredient import RecipeIngredient


@pytest.fixture
def sample_recipe() -> Recipe:
    return Recipe(
        id=UUID("12345678-1234-5678-1234-567812345678"),
        name="Spaghetti Carbonara",
        ingredients=[
            RecipeIngredient(name="Spaghetti", quantity=200.0, unit="g"),
            RecipeIngredient(name="Eggs", quantity=2.0, unit="pcs"),
            RecipeIngredient(name="Pancetta", quantity=100.0, unit="g"),
        ],
        instructions="Boil pasta, fry pancetta, mix with eggs and cheese.",
    )


@pytest.fixture
def sample_recipe_2() -> Recipe:
    return Recipe(
        id=UUID("87654321-4321-8765-4321-876543218765"),
        name="Tomato Soup",
        ingredients=[
            RecipeIngredient(name="Tomatoes", quantity=500.0, unit="g"),
            RecipeIngredient(name="Garlic", quantity=2.0, unit="cloves"),
        ],
        instructions="Blend tomatoes and garlic, simmer.",
    )


@pytest.fixture
def json_repo(tmp_path: Path) -> JsonRecipeRepository:
    file_path = tmp_path / "recipes.json"
    return JsonRecipeRepository(file_path=file_path)


def test_get_all_returns_empty_list_when_file_does_not_exist(json_repo):
    assert json_repo.get_all() == []


def test_save_and_get_all(json_repo, sample_recipe):
    json_repo.save(sample_recipe)
    recipes = json_repo.get_all()

    assert len(recipes) == 1
    assert recipes[0].id == sample_recipe.id
    assert recipes[0].name == sample_recipe.name
    assert len(recipes[0].ingredients) == 3


def test_get_all_skips_invalid_recipe_entry(json_repo, tmp_path, caplog):
    file_path = tmp_path / "recipes.json"
    file_path.write_text(
        json.dumps(
            [
                {"id": "invalid-uuid", "name": "Bad Recipe"},
                {
                    "id": "12345678-1234-5678-1234-567812345678",
                    "name": "Good Recipe",
                    "ingredients": [{"name": "Mehl", "quantity": 100.0, "unit": "g"}],
                    "instructions": "Verrühren und backen.",
                },
            ]
        ),
        encoding="utf-8",
    )

    with caplog.at_level(logging.ERROR):
        recipes = json_repo.get_all()

    assert len(recipes) == 1
    assert recipes[0].name == "Good Recipe"
    assert "Failed to deserialize entity" in caplog.text


def test_get_by_id_returns_recipe_when_found(json_repo, sample_recipe):
    json_repo.save(sample_recipe)
    found = json_repo.get_by_id(sample_recipe.id)

    assert found is not None
    assert found.id == sample_recipe.id


def test_get_by_id_returns_none_when_not_found(json_repo):
    assert json_repo.get_by_id(uuid4()) is None


def test_get_by_name_case_and_whitespace_insensitive(json_repo, sample_recipe):
    json_repo.save(sample_recipe)
    found = json_repo.get_by_name("  spaghetti CARBONARA  ")

    assert found is not None
    assert found.id == sample_recipe.id


def test_get_by_name_returns_none_when_not_found(json_repo):
    assert json_repo.get_by_name("Non Existent Recipe") is None


def test_filter_by_ingredients_returns_all_when_filter_empty(json_repo, sample_recipe):
    json_repo.save(sample_recipe)

    assert json_repo.filter_by_ingredients([]) == [sample_recipe]


def test_filter_by_ingredients_matches_subset(
    json_repo, sample_recipe, sample_recipe_2
):
    json_repo.save(sample_recipe)
    json_repo.save(sample_recipe_2)
    matches = json_repo.filter_by_ingredients(["spaghetti", " EGGS "])

    assert len(matches) == 1
    assert matches[0].id == sample_recipe.id


def test_filter_by_ingredients_returns_empty_when_no_match(json_repo, sample_recipe):
    json_repo.save(sample_recipe)
    matches = json_repo.filter_by_ingredients(["Chocolate", "Spaghetti"])

    assert matches == []


def test_save_updates_existing_recipe(json_repo, sample_recipe):
    json_repo.save(sample_recipe)
    updated_recipe = Recipe(
        id=sample_recipe.id,
        name="Spaghetti Carbonara Deluxe",
        ingredients=sample_recipe.ingredients,
        instructions="Updated instructions.",
    )
    json_repo.save(updated_recipe)
    recipes = json_repo.get_all()

    assert len(recipes) == 1
    assert recipes[0].name == "Spaghetti Carbonara Deluxe"
    assert recipes[0].instructions == "Updated instructions."


def test_delete_removes_recipe(json_repo, sample_recipe, sample_recipe_2):
    json_repo.save(sample_recipe)
    json_repo.save(sample_recipe_2)
    json_repo.delete(sample_recipe.id)
    recipes = json_repo.get_all()

    assert len(recipes) == 1
    assert recipes[0].id == sample_recipe_2.id
