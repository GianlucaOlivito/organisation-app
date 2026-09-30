import flet as ft

from app.adapters.ui.components.common.controls import (
    create_container,
    create_muted_text,
    create_search_button,
    create_text_field,
)
from app.adapters.ui.components.inventory.inventory_card import InventoryCard
from app.adapters.ui.components.inventory.inventory_filter_handler import (
    InventoryFilterHandler,
)
from app.adapters.ui.theme import theme
from app.application.inventory.search_service import InventorySearchService

from .base_view import BaseView


class InventoryView(BaseView):
    """Represents a view component for inventory management (UC-3.2)."""

    def __init__(
        self,
        search_service: InventorySearchService,
    ) -> None:
        self._filter_handler = InventoryFilterHandler(search_service)
        self._search_button = create_search_button(on_click=self._search)
        self._search_input = create_text_field(
            hint_text="Name oder ID",
            on_submit=self._search,
        )
        self._toolbar = ft.Row(
            controls=[self._search_button, self._search_input],
            spacing=theme.spacing_medium,
            vertical_alignment=ft.CrossAxisAlignment.CENTER,
        )
        self._empty_state = create_container(
            content=create_muted_text("Kein Vorrat gefunden"),
            alignment=ft.Alignment.CENTER,
            expand=True,
        )
        self._content_container = ft.Column(
            expand=True,
            alignment=ft.MainAxisAlignment.START,
            horizontal_alignment=ft.CrossAxisAlignment.STRETCH,
            controls=[self._empty_state],
        )
        super().__init__(title="Inventory")
        self._search()

    def _search(self, e: ft.ControlEvent | None = None) -> None:
        self._render_results(self._search_input.value or "")

    def _render_results(self, query: str | None) -> None:
        items = self._filter_handler.filter(query)
        if not items:
            self._content_container.controls = [self._empty_state]
        else:
            self._content_container.controls = [InventoryCard(inventory=items)]

    def _build_view(self) -> None:
        self.controls.extend([self._toolbar, self._content_container])
