from uuid import uuid4

import pytest

from app.application.recipes.modification_service import RecipeModificationService
from app.domain.recipes.recipe import Recipe
from app.domain.recipes.recipe_ingredient import RecipeIngredient


@pytest.fixture
def modification_service(fake_recipe_repo) -> RecipeModificationService:
    return RecipeModificationService(recipe_repository=fake_recipe_repo)


@pytest.fixture
def sample_recipe() -> Recipe:
    return Recipe(
        id=uuid4(),
        name="Spaghetti Carbonara",
        ingredients=[
            RecipeIngredient(name="Pasta", quantity=200.0, unit="g"),
            RecipeIngredient(name="Egg", quantity=2.0, unit=""),
        ],
    )


def test_create_recipe_success(modification_service, fake_recipe_repo, sample_recipe):
    created_recipe = modification_service.create(sample_recipe)

    assert created_recipe == sample_recipe
    assert fake_recipe_repo.get_by_id(sample_recipe.id) == sample_recipe


def test_create_recipe_already_exists_raises_error(
    modification_service, fake_recipe_repo, sample_recipe
):
    fake_recipe_repo.save(sample_recipe)

    with pytest.raises(
        ValueError,
        match=f"INVALID ARGUMENT: Recipe '{sample_recipe.name}' already exists.",
    ):
        modification_service.create(sample_recipe)


def test_modify_recipe_success(modification_service, fake_recipe_repo, sample_recipe):
    fake_recipe_repo.save(sample_recipe)
    updated_recipe = Recipe(
        id=sample_recipe.id,
        name="Spaghetti Carbonara Extra Cheese",
        ingredients=sample_recipe.ingredients,
    )
    modification_service.modify(updated_recipe)
    saved_recipe = fake_recipe_repo.get_by_id(sample_recipe.id)

    assert saved_recipe.name == "Spaghetti Carbonara Extra Cheese"


def test_modify_recipe_not_found_raises_error(modification_service, sample_recipe):
    with pytest.raises(
        ValueError,
        match=f"INVALID ARGUMENT: Recipe '{sample_recipe.name}' does not exist.",
    ):
        modification_service.modify(sample_recipe)


def test_delete_recipe_success(modification_service, fake_recipe_repo, sample_recipe):
    fake_recipe_repo.save(sample_recipe)

    modification_service.delete(sample_recipe.id)

    assert fake_recipe_repo.get_by_id(sample_recipe.id) is None


def test_delete_recipe_not_found_raises_error(modification_service):
    random_id = uuid4()

    with pytest.raises(
        ValueError, match=f"Recipe with ID '{random_id}' does not exist"
    ):
        modification_service.delete(random_id)
