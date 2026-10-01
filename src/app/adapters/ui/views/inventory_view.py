import flet as ft

from app.adapters.ui.components.common.controls import (
    create_add_button,
    create_container,
    create_muted_text,
    create_search_button,
    create_text_field,
)
from app.adapters.ui.components.inventory.inventory_card import InventoryCard
from app.adapters.ui.components.inventory.inventory_filter_handler import (
    InventoryFilterHandler,
)
from app.adapters.ui.components.inventory.inventory_form import InventoryForm
from app.adapters.ui.theme import theme
from app.application.inventory.modification_service import InventoryModificationService
from app.application.inventory.search_service import InventorySearchService
from app.domain.inventory.inventory_item import InventoryItem

from .base_view import BaseView


class InventoryView(BaseView):
    """Represents a view component for inventory management (UC-3.1 & UC-3.2)."""

    def __init__(
        self,
        modification_service: InventoryModificationService,
        search_service: InventorySearchService,
    ) -> None:
        self._modification_service = modification_service
        self._search_service = search_service
        self._filter_handler = InventoryFilterHandler(search_service)

        self._add_button = create_add_button(on_click=lambda _: self._open_form())
        self._search_button = create_search_button(on_click=self._search)
        self._search_input = create_text_field(
            hint_text="Name oder ID",
            on_submit=self._search,
        )
        self._toolbar = ft.Row(
            controls=[self._add_button, self._search_button, self._search_input],
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

    def _close_form(self) -> None:
        self._toolbar.visible = True
        self._search()

    def _open_form(self, inventory: list[InventoryItem] | None = None) -> None:
        existing_items = {item.id: item for item in self._search_service.get_all()}

        def _handle_save(saved_inventory: list[InventoryItem]) -> None:
            saved_ids = {item.id for item in saved_inventory}
            for item_id in set(existing_items.keys()) - saved_ids:
                self._modification_service.delete(item_id)
            for item in saved_inventory:
                if item.id in existing_items:
                    self._modification_service.modify(item)
                else:
                    self._modification_service.create(item)
            self._close_form()

        self._toolbar.visible = False
        self._content_container.controls = [
            InventoryForm(
                inventory=inventory or [],
                on_save=_handle_save,
                on_close=self._close_form,
            )
        ]
        self.update()

    def _render_results(self, query: str | None) -> None:
        items = self._filter_handler.filter(query)
        if not items:
            self._add_button.visible = True
            self._content_container.controls = [self._empty_state]
        else:
            self._add_button.visible = False
            self._content_container.controls = [
                InventoryCard(
                    inventory=items,
                    on_edit=lambda items_to_edit: self._open_form(items_to_edit),
                )
            ]

    def _build_view(self) -> None:
        self.controls.extend([self._toolbar, self._content_container])
