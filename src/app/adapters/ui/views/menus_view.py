from uuid import UUID

import flet as ft

from app.adapters.ui.components.common.controls import (
    create_add_button,
    create_filter_button,
    create_search_button,
    create_text_field,
)
from app.adapters.ui.components.meal_planning.menu_card import MenuCard
from app.adapters.ui.components.meal_planning.menu_filter_handler import (
    MenuFilterHandler,
)
from app.adapters.ui.components.meal_planning.menu_form import MenuForm
from app.adapters.ui.theme import theme
from app.application.meal_planning.modification_service import MenuModificationService
from app.application.meal_planning.search_service import MenuSearchService
from app.application.recipes.search_service import RecipeSearchService
from app.domain.meal_planning.menu import Menu

from .entity_view import EntityView


class MenusView(EntityView[Menu]):
    """Represents a view component for meal planning (UC-2.1 & UC-2.2)."""

    def __init__(
        self,
        modification_service: MenuModificationService,
        menu_search_service: MenuSearchService,
        recipe_search_service: RecipeSearchService,
    ) -> None:
        self._modification_service = modification_service
        self._recipe_search_service = recipe_search_service
        self._filter_handler = MenuFilterHandler(menu_search_service)
        self._grid = ft.GridView(
            expand=True,
            max_extent=theme.grid_max_extent,
            child_aspect_ratio=theme.grid_aspect_ratio,
            spacing=theme.spacing_medium,
            run_spacing=theme.spacing_medium,
        )
        super().__init__(title="Menüplanung", empty_text="Keine Menüs gefunden")

    def _build_toolbar(self) -> ft.Row:
        self._add_button = create_add_button(on_click=lambda _: self._open_form())
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
        return ft.Row(
            controls=[
                self._add_button,
                self._search_button,
                self._search_input,
                self._filter_button,
                self._start_date_input,
                self._end_date_input,
            ],
            spacing=theme.spacing_medium,
            vertical_alignment=ft.CrossAxisAlignment.CENTER,
        )

    def _search(self, e: ft.ControlEvent | None = None) -> None:
        self._render_results(query=self._search_input.value or "")

    def _filter(self, e: ft.ControlEvent | None = None) -> None:
        self._render_results(
            start_date=self._start_date_input.value or "",
            end_date=self._end_date_input.value or "",
        )

    def _delete_menu(self, menu_id: UUID) -> None:
        self._modification_service.delete(menu_id)
        self._search()

    def _create_form(
        self,
        entity: Menu | None,
        on_save: callable,
        on_close: callable,
    ) -> ft.Control:
        return MenuForm(menu=entity, on_save=on_save, on_close=on_close)

    def _save_entity(self, entity: Menu, is_edit: bool) -> None:
        if is_edit:
            self._modification_service.modify(entity)
        else:
            self._modification_service.create(entity)

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
                MenuCard(
                    menu=m,
                    recipe_search_service=self._recipe_search_service,
                    on_edit=lambda menu=m: self._open_form(menu),
                    on_delete=lambda menu_id=m.id: self._delete_menu(menu_id),
                )
                for m in menus
            ]
            self._content_container.controls = [self._grid]
