from uuid import UUID

import pytest

from app.application.recipes.repository import RecipeRepository
from app.domain.recipes.recipe import Recipe


class FakeRecipeRepository(RecipeRepository):
    """In-memory implementation of RecipeRepository for fast unit testing."""

    def __init__(self) -> None:
        self._recipes: dict[UUID, Recipe] = {}

    def get_all(self) -> list[Recipe]:
        return list(self._recipes.values())

    def get_by_id(self, id: UUID) -> Recipe | None:
        return self._recipes.get(id)

    def get_by_name(self, name: str) -> Recipe | None:
        return next((r for r in self._recipes.values() if r.name == name), None)

    def filter_by_ingredients(self, ingredients: list[str]) -> list[Recipe]:
        target_ingredients = {i.lower() for i in ingredients}
        return [
            recipe
            for recipe in self._recipes.values()
            if target_ingredients.issubset(
                {ing.name.lower() for ing in recipe.ingredients}
            )
        ]

    def save(self, recipe: Recipe) -> None:
        self._recipes[recipe.id] = recipe

    def delete(self, id: UUID) -> None:
        self._recipes.pop(id, None)


@pytest.fixture
def fake_recipe_repo() -> FakeRecipeRepository:
    """Fixture providing a fresh in-memory repository for each test."""

    return FakeRecipeRepository()
