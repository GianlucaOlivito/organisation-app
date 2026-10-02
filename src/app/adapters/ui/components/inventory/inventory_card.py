from collections.abc import Callable

import flet as ft

from app.adapters.ui.components.common.base_card import BaseCard
from app.adapters.ui.components.common.controls import (
    create_divider,
    create_muted_text,
    create_text,
)
from app.adapters.ui.theme import theme
from app.domain.inventory.inventory_item import InventoryItem


class InventoryCard(BaseCard[list[InventoryItem]]):
    """Represents a component to display the whole inventory."""

    def __init__(
        self,
        inventory: list[InventoryItem],
        on_edit: Callable[[list[InventoryItem]], None] | None = None,
    ) -> None:
        self.inventory = inventory
        super().__init__(entity=inventory, on_edit=on_edit, on_delete=None)

    def _build_inventory_rows(self) -> list[ft.Control]:
        rows: list[ft.Control] = []
        for item in self.inventory:
            qty = int(item.quantity) if item.quantity.is_integer() else item.quantity
            unit_str = item.unit if item.unit else ""
            row = ft.Row(
                controls=[
                    create_muted_text(str(item.id)[:8], width=theme.col_width_small),
                    create_text(
                        f"{qty} {unit_str}".strip(), width=theme.col_width_small
                    ),
                    create_text(item.name, expand=True),
                ],
                alignment=ft.MainAxisAlignment.START,
                vertical_alignment=ft.CrossAxisAlignment.CENTER,
            )
            rows.append(row)
        return rows

    def _build_inventory_section(self) -> ft.Control:
        return ft.Column(
            controls=self._build_inventory_rows(),
            spacing=theme.spacing_small,
        )

    def _build_card_content(self) -> list[ft.Control]:
        return [
            self._build_header(title="Vorrat"),
            create_divider(),
            self._build_inventory_section(),
        ]
