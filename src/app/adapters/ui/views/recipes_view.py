from uuid import UUID

import flet as ft

from app.adapters.ui.components.common.controls import (
    create_add_button,
    create_filter_button,
    create_search_button,
    create_text_field,
)
from app.adapters.ui.components.recipes.recipe_card import RecipeCard
from app.adapters.ui.components.recipes.recipe_filter_handler import RecipeFilterHandler
from app.adapters.ui.components.recipes.recipe_form import RecipeForm
from app.adapters.ui.theme import theme
from app.application.recipes.modification_service import RecipeModificationService
from app.application.recipes.search_service import RecipeSearchService
from app.domain.recipes.recipe import Recipe

from .entity_view import EntityView


class RecipesView(EntityView[Recipe]):
    """Represents a view component for recipe management (UC-1.1 & UC-1.2)."""

    def __init__(
        self,
        modification_service: RecipeModificationService,
        search_service: RecipeSearchService,
    ) -> None:
        self._modification_service = modification_service
        self._filter_handler = RecipeFilterHandler(search_service)
        self._grid = ft.GridView(
            expand=True,
            max_extent=theme.grid_max_extent,
            child_aspect_ratio=theme.grid_aspect_ratio,
            spacing=theme.spacing_medium,
            run_spacing=theme.spacing_medium,
        )
        super().__init__(title="Rezepte", empty_text="Keine Rezepte gefunden")

    def _build_toolbar(self) -> ft.Row:
        self._add_button = create_add_button(on_click=lambda _: self._open_form())
        self._search_button = create_search_button(on_click=self._search)
        self._search_input = create_text_field(
            hint_text="Name oder ID",
            on_submit=self._search,
        )
        self._filter_button = create_filter_button(on_click=self._filter)
        self._ingredient_input = create_text_field(
            hint_text="Zutaten (kommagetrennt)",
            on_submit=self._filter,
        )
        return ft.Row(
            controls=[
                self._add_button,
                self._search_button,
                self._search_input,
                self._filter_button,
                self._ingredient_input,
            ],
            spacing=theme.spacing_medium,
            vertical_alignment=ft.CrossAxisAlignment.CENTER,
        )

    def _search(self, e: ft.ControlEvent | None = None) -> None:
        self._render_results(self._search_input.value or "", None)

    def _filter(self, e: ft.ControlEvent | None = None) -> None:
        self._render_results(None, self._ingredient_input.value or "")

    def _delete_recipe(self, recipe_id: UUID) -> None:
        self._modification_service.delete(recipe_id)
        self._search()

    def _create_form(
        self,
        entity: Recipe | None,
        on_save: callable,
        on_close: callable,
    ) -> ft.Control:
        return RecipeForm(recipe=entity, on_save=on_save, on_close=on_close)

    def _save_entity(self, entity: Recipe, is_edit: bool) -> None:
        if is_edit:
            self._modification_service.modify(entity)
        else:
            self._modification_service.create(entity)

    def _render_results(self, query: str | None, ing_query: str | None) -> None:
        recipes = self._filter_handler.filter(query, ing_query)
        if not recipes:
            self._content_container.controls = [self._empty_state]
        else:
            self._grid.controls = [
                RecipeCard(
                    recipe=r,
                    on_edit=lambda recipe=r: self._open_form(recipe),
                    on_delete=lambda recipe_id=r.id: self._delete_recipe(recipe_id),
                )
                for r in recipes
            ]
            self._content_container.controls = [self._grid]
