from collections.abc import Callable

import flet as ft

from app.adapters.ui.components.common.base_card import BaseCard
from app.adapters.ui.components.common.controls import (
    create_close_button,
    create_divider,
    create_icon_button,
    create_text,
)
from app.adapters.ui.theme import theme
from app.domain.inventory.shopping_list import ShoppingList


class ShoppingListCard(BaseCard[ShoppingList]):
    """Represents a component to display a generated shopping list."""

    def __init__(
        self,
        shopping_list: ShoppingList,
        on_apply: Callable[[ShoppingList], None] | None = None,
        on_export: Callable[[], None] | None = None,
        on_clear: Callable[[], None] | None = None,
    ) -> None:
        self.on_apply = on_apply
        self.on_export = on_export
        self.on_clear = on_clear
        super().__init__(entity=shopping_list, on_edit=None, on_delete=None)

    def _build_header_actions(self) -> list[ft.Control]:
        actions: list[ft.Control] = []
        if self.on_apply:
            actions.append(
                create_icon_button(
                    icon=ft.Icons.CHECKLIST_ROUNDED,
                    icon_color=theme.color_active,
                    tooltip="Einkauf verbuchen",
                    on_click=lambda _: self.on_apply(self.entity),
                )
            )
        if self.on_export:
            actions.append(
                create_icon_button(
                    icon=ft.Icons.IOS_SHARE,
                    icon_color=theme.color_active,
                    tooltip="Einkaufsliste exportieren",
                    on_click=lambda _: self.on_export(),
                )
            )
        if self.on_clear:
            actions.append(
                create_close_button(
                    tooltip="Einkaufsliste verwerfen",
                    on_click=lambda _: self.on_clear(),
                )
            )
        return actions

    def _build_shopping_list_rows(self) -> list[ft.Control]:
        rows: list[ft.Control] = []
        for item in self.entity.items:
            qty = int(item.quantity) if item.quantity.is_integer() else item.quantity
            unit_str = item.unit if item.unit else ""
            row = ft.Row(
                controls=[
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

    def _build_shopping_list_section(self) -> ft.Control:
        return ft.Column(
            controls=self._build_shopping_list_rows(),
            spacing=theme.spacing_small,
        )

    def _build_card_content(self) -> list[ft.Control]:
        return [
            self._build_header(
                title="Einkaufsliste",
                custom_actions=self._build_header_actions(),
            ),
            create_divider(),
            self._build_shopping_list_section(),
        ]
