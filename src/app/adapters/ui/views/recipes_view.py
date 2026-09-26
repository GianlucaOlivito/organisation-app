from uuid import UUID

import flet as ft

from app.adapters.ui.components.common.controls import (
    create_add_button,
    create_container,
    create_filter_button,
    create_muted_text,
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

from .base_view import BaseView


class RecipesView(BaseView):
    """Represents a view component for recipe management (UC-1.1 & UC-1.2)."""

    def __init__(
        self,
        modification_service: RecipeModificationService,
        search_service: RecipeSearchService,
    ) -> None:
        self._modification_service = modification_service
        self._filter_handler = RecipeFilterHandler(search_service)
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
        self._toolbar = ft.Row(
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
        self._grid = ft.GridView(
            expand=True,
            max_extent=theme.grid_max_extent,
            child_aspect_ratio=theme.grid_aspect_ratio,
            spacing=theme.spacing_medium,
            run_spacing=theme.spacing_medium,
        )
        self._empty_state = create_container(
            content=create_muted_text("Keine Rezepte gefunden"),
            alignment=ft.Alignment.CENTER,
            expand=True,
        )
        self._content_container = ft.Column(
            expand=True,
            alignment=ft.MainAxisAlignment.START,
            horizontal_alignment=ft.CrossAxisAlignment.STRETCH,
            controls=[self._empty_state],
        )
        super().__init__(title="Recipes")
        self._search()

    def _search(self, e: ft.ControlEvent | None = None) -> None:
        self._render_results(self._search_input.value or "", None)

    def _filter(self, e: ft.ControlEvent | None = None) -> None:
        self._render_results(None, self._ingredient_input.value or "")

    def _delete_recipe(self, recipe_id: UUID) -> None:
        self._modification_service.delete(recipe_id)
        self._search()

    def _close_form(self) -> None:
        self._toolbar.visible = True
        self._search()

    def _open_form(self, recipe: Recipe | None = None) -> None:
        def _handle_save(saved_recipe: Recipe) -> None:
            if recipe is not None:
                self._modification_service.modify(saved_recipe)
            else:
                self._modification_service.create(saved_recipe)
            self._close_form()

        self._toolbar.visible = False
        self._content_container.controls = [
            RecipeForm(recipe=recipe, on_save=_handle_save, on_close=self._close_form)
        ]
        self.update()

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

    def _build_view(self) -> None:
        self.controls.extend([self._toolbar, self._content_container])
