import flet as ft

from app.adapters.ui.components.common.controls import (
    create_container,
    create_icon_button,
    create_muted_text,
    create_text_field,
)
from app.adapters.ui.components.common.filter_helpers import parse_str_to_date
from app.adapters.ui.components.inventory.shopping_list_card import ShoppingListCard
from app.adapters.ui.components.inventory.shopping_list_filter_handler import (
    ShoppingListFilterHandler,
)
from app.adapters.ui.theme import theme
from app.application.inventory.reconciliation_service import (
    InventoryReconciliationService,
)
from app.application.inventory.shopping_list_service import ShoppingListService
from app.config.settings import Settings
from app.domain.inventory.shopping_list import ShoppingList

from .base_view import BaseView


class ShoppingListView(BaseView):
    """Represents a view component for shopping list management (UC-3.3)."""

    def __init__(
        self,
        settings: Settings,
        shopping_list_service: ShoppingListService,
        inventory_reconciliation_service: InventoryReconciliationService,
    ) -> None:
        self._settings = settings
        self._shopping_list_service = shopping_list_service
        self._inventory_reconciliation_service = inventory_reconciliation_service
        self._filter_handler = ShoppingListFilterHandler(shopping_list_service)
        self._shopping_list: ShoppingList | None = None
        self._empty_state = create_container(
            content=create_muted_text("Keine Einkaufsliste gefunden"),
            alignment=ft.Alignment.CENTER,
            expand=True,
        )
        self._content_container = ft.Column(
            expand=True,
            alignment=ft.MainAxisAlignment.START,
            horizontal_alignment=ft.CrossAxisAlignment.STRETCH,
            controls=[self._empty_state],
        )
        self._toolbar = self._build_toolbar()
        super().__init__(title="Einkauf")

    def _build_toolbar(self) -> ft.Row:
        self._generate_shopping_list_button = create_icon_button(
            icon=ft.Icons.SHOPPING_CART_ROUNDED,
            icon_color=theme.color_active,
            tooltip="Einkaufsliste generieren",
            on_click=self._filter,
        )
        self._start_date_input = create_text_field(hint_text="Startdatum (DD.MM.YYYY)")
        self._end_date_input = create_text_field(hint_text="Enddatum (DD.MM.YYYY)")
        self._consume_meals_button = create_icon_button(
            icon=ft.Icons.TABLE_RESTAURANT_ROUNDED,
            icon_color=theme.color_active,
            tooltip="Mahlzeiten konsumieren",
            on_click=self._handle_consume_meals,
        )
        return ft.Row(
            controls=[
                self._generate_shopping_list_button,
                self._consume_meals_button,
                self._start_date_input,
                self._end_date_input,
            ],
            spacing=theme.spacing_medium,
            vertical_alignment=ft.CrossAxisAlignment.CENTER,
        )

    def _handle_consume_meals(self, e: ft.ControlEvent | None = None) -> None:
        start_date = parse_str_to_date(self._start_date_input.value)
        end_date = parse_str_to_date(self._end_date_input.value)
        if not start_date or not end_date:
            return
        try:
            self._inventory_reconciliation_service.consume_meals_for_period(
                start_date=start_date,
                end_date=end_date,
            )
        except ValueError:
            return
        return

    def _clear_list(self) -> None:
        self._shopping_list = None
        self._content_container.controls = [self._empty_state]
        self.update()

    def _handle_apply_shopping_list(self, shopping_list: ShoppingList) -> None:
        self._inventory_reconciliation_service.apply_shopping_list(shopping_list)
        self._clear_list()

    def _render_results(self, start_date: str | None, end_date: str | None) -> None:
        shopping_list = self._filter_handler.filter(
            start_date=start_date, end_date=end_date
        )
        if not shopping_list or not shopping_list.items:
            self._clear_list()
            return
        self._shopping_list = shopping_list
        self._content_container.controls = [
            ShoppingListCard(
                shopping_list=shopping_list,
                on_apply=self._handle_apply_shopping_list,
                on_clear=self._clear_list,
            )
        ]
        self.update()

    def _filter(self, e: ft.ControlEvent | None = None) -> None:
        self._render_results(
            start_date=self._start_date_input.value or "",
            end_date=self._end_date_input.value or "",
        )

    def _build_view(self) -> None:
        self.controls.extend([self._toolbar, self._content_container])
