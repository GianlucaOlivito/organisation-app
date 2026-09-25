import flet as ft

from app.adapters.ui.components.common.controls import (
    create_container,
    create_filter_button,
    create_muted_text,
    create_search_button,
    create_text_field,
)
from app.adapters.ui.components.recipes.recipe_card import RecipeCard
from app.adapters.ui.components.recipes.recipe_filter_handler import RecipeFilterHandler
from app.adapters.ui.theme import theme
from app.application.recipes.modification_service import RecipeModificationService
from app.application.recipes.search_service import RecipeSearchService

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

    def _render_results(self, query: str | None, ing_query: str | None) -> None:
        recipes = self._filter_handler.filter(query, ing_query)
        if not recipes:
            self._content_container.controls = [self._empty_state]
        else:
            self._grid.controls = [RecipeCard(r) for r in recipes]
            self._content_container.controls = [self._grid]

    def _build_view(self) -> None:
        toolbar = ft.Row(
            controls=[
                self._search_button,
                self._search_input,
                self._filter_button,
                self._ingredient_input,
            ],
            spacing=theme.spacing_medium,
            vertical_alignment=ft.CrossAxisAlignment.CENTER,
        )
        self.controls.extend([toolbar, self._content_container])
