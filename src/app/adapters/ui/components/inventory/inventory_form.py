from collections.abc import Callable
from uuid import UUID, uuid4

import flet as ft

from app.adapters.ui.components.common.base_form import BaseForm
from app.adapters.ui.components.common.controls import (
    create_add_button,
    create_container,
    create_delete_button,
    create_text_field,
)
from app.adapters.ui.theme import theme
from app.domain.inventory.inventory_item import InventoryItem


class InventoryForm(BaseForm[list[InventoryItem]]):
    """Represents a form component for modifying the inventory."""

    def __init__(
        self,
        inventory: list[InventoryItem] | None = None,
        on_save: Callable[[list[InventoryItem]], None] | None = None,
        on_close: Callable[[], None] | None = None,
    ) -> None:
        self._inventory = inventory or []
        self._items_column = ft.Column(spacing=theme.spacing_small)
        extra_header = [
            create_add_button(on_click=lambda _: (self._add_item_row(), self.update()))
        ]
        super().__init__(
            title="Vorrat modifizieren",
            on_save=on_save,
            on_close=on_close,
            extra_header_controls=extra_header,
        )

    def _add_item_row(
        self,
        item_id: UUID | None = None,
        name: str = "",
        quantity: str = "",
        unit: str = "",
    ) -> None:
        name_field = create_text_field(hint_text="Name", value=name)
        qty_field = create_text_field(hint_text="Menge", value=quantity)
        unit_field = create_text_field(hint_text="Einheit", value=unit)
        row = ft.Row(spacing=theme.spacing_small, data=item_id or uuid4())

        def _delete_row(_: ft.ControlEvent) -> None:
            self._items_column.controls.remove(row)
            self.update()

        del_btn = create_delete_button(on_click=_delete_row)
        row.controls = [name_field, qty_field, unit_field, del_btn]
        self._items_column.controls.append(row)

    def _extract_entity(self) -> list[InventoryItem]:
        items: list[InventoryItem] = []
        for row in self._items_column.controls:
            if not isinstance(row, ft.Row):
                continue
            name = (row.controls[0].value or "").strip()
            qty = (row.controls[1].value or "").strip()
            unit = (row.controls[2].value or "").strip()
            if not name and not qty and not unit:
                continue
            items.append(InventoryItem(id=row.data, name=name, quantity=qty, unit=unit))
        return items

    def _build_form_controls(self) -> list[ft.Control]:
        items_container = create_container(
            content=self._items_column,
            padding=theme.spacing_none,
        )
        if self._inventory:
            for item in self._inventory:
                self._add_item_row(
                    item_id=item.id,
                    name=item.name,
                    quantity=str(item.quantity),
                    unit=item.unit or "",
                )
        else:
            self._add_item_row()
        return [items_container]
