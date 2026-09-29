import flet as ft

from app.adapters.ui.components.common.controls import (
    create_container,
    create_filter_button,
    create_muted_text,
    create_search_button,
    create_text_field,
)
from app.adapters.ui.components.meal_planning.menu_card import MenuCard
from app.adapters.ui.components.meal_planning.menu_filter_handler import (
    MenuFilterHandler,
)
from app.adapters.ui.theme import theme
from app.application.meal_planning.search_service import MenuSearchService
from app.application.recipes.search_service import RecipeSearchService

from .base_view import BaseView


class MenusView(BaseView):
    """Represents a view component for meal planning (UC-2.2)."""

    def __init__(
        self,
        menu_search_service: MenuSearchService,
        recipe_search_service: RecipeSearchService,
    ) -> None:
        self._recipe_search_service = recipe_search_service
        self._filter_handler = MenuFilterHandler(menu_search_service)
        self._search_button = create_search_button(on_click=self._search)
        self._search_input = create_text_field(
            hint_text="ID",
            on_submit=self._search,
        )
        self._filter_button = create_filter_button(on_click=self._filter)
        self._start_date_input = create_text_field(
            hint_text="Startdatum (DD.MM.YYYY)",
            on_submit=self._filter,
        )
        self._end_date_input = create_text_field(
            hint_text="Enddatum (DD.MM.YYYY)",
            on_submit=self._filter,
        )
        self._toolbar = ft.Row(
            controls=[
                self._search_button,
                self._search_input,
                self._filter_button,
                self._start_date_input,
                self._end_date_input,
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
            content=create_muted_text("Keine Menüs gefunden"),
            alignment=ft.Alignment.CENTER,
            expand=True,
        )
        self._content_container = ft.Column(
            expand=True,
            alignment=ft.MainAxisAlignment.START,
            horizontal_alignment=ft.CrossAxisAlignment.STRETCH,
            controls=[self._empty_state],
        )
        super().__init__(title="Meal Planning")
        self._search()

    def _search(self, e: ft.ControlEvent | None = None) -> None:
        self._render_results(query=self._search_input.value or "")

    def _filter(self, e: ft.ControlEvent | None = None) -> None:
        self._render_results(
            start_date=self._start_date_input.value or "",
            end_date=self._end_date_input.value or "",
        )

    def _render_results(
        self,
        query: str | None = None,
        start_date: str | None = None,
        end_date: str | None = None,
    ) -> None:
        menus = self._filter_handler.filter(query, start_date, end_date)
        if not menus:
            self._content_container.controls = [self._empty_state]
        else:
            self._grid.controls = [
                MenuCard(m, self._recipe_search_service) for m in menus
            ]
            self._content_container.controls = [self._grid]

    def _build_view(self) -> None:
        self.controls.extend([self._toolbar, self._content_container])
