import json
import logging
from uuid import uuid4

from app.domain.recipes.recipe import Recipe


def test_get_all_returns_empty_list_when_file_does_not_exist(json_recipe_repo):
    assert json_recipe_repo.get_all() == []


def test_save_and_get_all(json_recipe_repo, sample_recipes):
    sample_recipe = sample_recipes[0]
    json_recipe_repo.save(sample_recipe)
    recipes = json_recipe_repo.get_all()

    assert len(recipes) == 1
    assert recipes[0].id == sample_recipe.id
    assert recipes[0].name == sample_recipe.name
    assert len(recipes[0].ingredients) == len(sample_recipe.ingredients)


def test_get_all_skips_invalid_recipe_entry(json_recipe_repo, tmp_path, caplog):
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
        recipes = json_recipe_repo.get_all()

    assert len(recipes) == 1
    assert recipes[0].name == "Good Recipe"
    assert "Failed to deserialize entity" in caplog.text


def test_get_by_id_returns_recipe_when_found(json_recipe_repo, sample_recipes):
    sample_recipe = sample_recipes[0]
    json_recipe_repo.save(sample_recipe)
    found = json_recipe_repo.get_by_id(sample_recipe.id)

    assert found is not None
    assert found.id == sample_recipe.id


def test_get_by_id_returns_none_when_not_found(json_recipe_repo):
    assert json_recipe_repo.get_by_id(uuid4()) is None


def test_get_by_name_case_and_whitespace_insensitive(json_recipe_repo, sample_recipes):
    sample_recipe = sample_recipes[0]
    json_recipe_repo.save(sample_recipe)
    found = json_recipe_repo.get_by_name("  spaghetti CARBONARA  ")

    assert found is not None
    assert found.id == sample_recipe.id


def test_get_by_name_returns_none_when_not_found(json_recipe_repo):
    assert json_recipe_repo.get_by_name("Non Existent Recipe") is None


def test_filter_by_ingredients_returns_all_when_filter_empty(
    json_recipe_repo, sample_recipes
):
    sample_recipe = sample_recipes[0]
    json_recipe_repo.save(sample_recipe)

    assert json_recipe_repo.filter_by_ingredients([]) == [sample_recipe]


def test_filter_by_ingredients_matches_subset(json_recipe_repo, sample_recipes):
    recipe1, recipe2 = sample_recipes
    json_recipe_repo.save(recipe1)
    json_recipe_repo.save(recipe2)
    matches = json_recipe_repo.filter_by_ingredients(["pasta", " EGGS "])

    assert len(matches) == 1
    assert matches[0].id == recipe1.id


def test_filter_by_ingredients_returns_empty_when_no_match(
    json_recipe_repo, sample_recipes
):
    sample_recipe = sample_recipes[0]
    json_recipe_repo.save(sample_recipe)
    matches = json_recipe_repo.filter_by_ingredients(["Chocolate", "Spaghetti"])

    assert matches == []


def test_save_updates_existing_recipe(json_recipe_repo, sample_recipes):
    sample_recipe = sample_recipes[0]
    json_recipe_repo.save(sample_recipe)
    updated_recipe = Recipe(
        id=sample_recipe.id,
        name="Spaghetti Carbonara Deluxe",
        ingredients=sample_recipe.ingredients,
        instructions="Updated instructions.",
    )
    json_recipe_repo.save(updated_recipe)
    recipes = json_recipe_repo.get_all()

    assert len(recipes) == 1
    assert recipes[0].name == "Spaghetti Carbonara Deluxe"
    assert recipes[0].instructions == "Updated instructions."


def test_delete_removes_recipe(json_recipe_repo, sample_recipes):
    recipe1, recipe2 = sample_recipes
    json_recipe_repo.save(recipe1)
    json_recipe_repo.save(recipe2)
    json_recipe_repo.delete(recipe1.id)
    recipes = json_recipe_repo.get_all()

    assert len(recipes) == 1
    assert recipes[0].id == recipe2.id
