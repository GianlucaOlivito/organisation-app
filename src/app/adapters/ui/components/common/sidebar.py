from collections.abc import Callable

import flet as ft

from app.adapters.ui.components.common.controls import create_container, create_text
from app.adapters.ui.theme import theme


class Sidebar(ft.Column):
    """Represents sidebar for menu navigation managing tabs and selection state."""

    def __init__(
        self,
        items: list[tuple[str, str]],
        selected_index: int = 0,
        on_change: Callable[[int], None] | None = None,
    ) -> None:
        self._on_change = on_change
        self._selected_index = selected_index
        self._tab_refs: list[tuple[ft.Icon, ft.Text]] = []
        controls: list[ft.Control] = []
        for i, (icon, label) in enumerate(items):
            is_selected = i == selected_index
            color = theme.color_active if is_selected else theme.color_inactive
            icon_ctrl = ft.Icon(icon, color=color)
            text_ctrl = create_text(label, size=theme.font_size_small, color=color)
            self._tab_refs.append((icon_ctrl, text_ctrl))
            tab_container = create_container(
                content=ft.Column(
                    spacing=theme.spacing_small,
                    horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                    controls=[icon_ctrl, text_ctrl],
                ),
                padding=theme.spacing_medium,
                ink=True,
                on_click=lambda _, idx=i: self._handle_select(idx),
            )
            controls.append(tab_container)
        super().__init__(
            alignment=ft.MainAxisAlignment.SPACE_EVENLY,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            width=theme.sidebar_width,
            controls=controls,
        )

    def _handle_select(self, index: int) -> None:
        if index == self._selected_index:
            return
        old_icon, old_text = self._tab_refs[self._selected_index]
        old_icon.color = old_text.color = theme.color_inactive
        new_icon, new_text = self._tab_refs[index]
        new_icon.color = new_text.color = theme.color_active
        self._selected_index = index
        self.update()
        if self._on_change:
            self._on_change(index)
