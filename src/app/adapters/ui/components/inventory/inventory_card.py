from collections.abc import Callable

import flet as ft

from app.adapters.ui.components.common.controls import (
    create_container,
    create_divider,
    create_edit_button,
    create_header,
    create_text,
)
from app.adapters.ui.theme import theme
from app.domain.inventory.inventory_item import InventoryItem


class InventoryCard(ft.Card):
    """
    Represents a component to display the inventory as a table of InventoryItem entities.
    """

    def __init__(
        self,
        inventory: list[InventoryItem],
        on_edit: Callable[[list[InventoryItem]], None] | None = None,
    ) -> None:
        self.inventory = inventory
        self.on_edit = on_edit
        super().__init__(
            content=create_container(
                content=ft.Column(
                    controls=[
                        self._build_header(),
                        create_divider(),
                        self._build_inventory_section(),
                    ],
                    spacing=theme.spacing_medium,
                    scroll=ft.ScrollMode.AUTO,
                    expand=True,
                ),
            )
        )

    @staticmethod
    def _format_inventory_item(item: InventoryItem) -> str:
        id = str(item.id)[:8]
        qty = int(item.quantity) if item.quantity.is_integer() else item.quantity
        unit_str = f" {item.unit}" if item.unit else ""
        return f"{id}\t{qty}\t{unit_str}\t{item.name}"

    def _build_header(self) -> ft.Control:
        controls: list[ft.Control] = [create_header("Vorrat", expand=True)]
        if self.on_edit is not None:
            controls.append(
                create_edit_button(on_click=lambda _: self.on_edit(self.inventory))
            )
        return ft.Row(controls=controls, alignment=ft.MainAxisAlignment.SPACE_BETWEEN)

    def _build_inventory_rows(self) -> list[ft.Control]:
        rows: list[ft.Control] = []
        for item in self.inventory:
            row = ft.Row(
                controls=[
                    create_text(
                        self._format_inventory_item(item), size=theme.font_size_small
                    )
                ],
                alignment=ft.MainAxisAlignment.START,
            )
            rows.append(row)
        return rows

    def _build_inventory_section(self) -> ft.Control:
        return ft.Column(
            controls=self._build_inventory_rows(),
            spacing=theme.spacing_small,
        )
