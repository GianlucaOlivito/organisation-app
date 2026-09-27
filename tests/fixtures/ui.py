from unittest.mock import MagicMock

import pytest

from app.adapters.ui.components.recipes.recipe_filter_handler import RecipeFilterHandler
from app.adapters.ui.components.recipes.recipe_form import RecipeForm
from app.adapters.ui.views.logs_view import LogsView
from app.adapters.ui.views.recipes_view import RecipesView
from app.application.recipes.modification_service import RecipeModificationService
from app.application.recipes.search_service import RecipeSearchService
from app.domain.recipes.recipe import Recipe
from app.infrastructure.log_buffer import LogBuffer


@pytest.fixture
def populated_search_service(
    recipes_search_service: RecipeSearchService,
    sample_recipes: list[Recipe],
) -> RecipeSearchService:
    for recipe in sample_recipes:
        recipes_search_service._recipe_repository.save(recipe)
    return recipes_search_service


@pytest.fixture
def recipe_filter_handler(
    populated_search_service: RecipeSearchService,
) -> RecipeFilterHandler:
    return RecipeFilterHandler(search_service=populated_search_service)


@pytest.fixture
def recipe_form() -> RecipeForm:
    form = RecipeForm()
    form.update = MagicMock()
    return form


@pytest.fixture
def logs_view(log_buffer: LogBuffer) -> LogsView:
    return LogsView(log_buffer=log_buffer)


@pytest.fixture
def recipes_view(
    recipes_modification_service: RecipeModificationService,
    populated_search_service: RecipeSearchService,
) -> RecipesView:
    view = RecipesView(
        modification_service=recipes_modification_service,
        search_service=populated_search_service,
    )
    view.update = MagicMock()
    return view
