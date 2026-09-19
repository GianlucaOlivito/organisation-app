from collections.abc import Callable

import flet as ft


class NavigationTab(ft.Container):
    """Represents a self-contained sidebar navigation tab control."""

    def __init__(
        self,
        index: int,
        icon: str,
        label: str,
        is_selected: bool,
        on_select: Callable[[int], None],
    ) -> None:
        self.index = index
        self._on_select = on_select
        color = ft.Colors.PRIMARY if is_selected else ft.Colors.ON_SURFACE_VARIANT
        self._icon_control = ft.Icon(icon, color=color)
        self._text_control = ft.Text(label, size=12, color=color)
        super().__init__(
            content=ft.Column(
                spacing=4,
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                controls=[self._icon_control, self._text_control],
            ),
            padding=10,
            border_radius=8,
            ink=True,
            on_click=lambda _: self._on_select(self.index),
        )

    def set_active(self, is_selected: bool) -> None:
        color = ft.Colors.PRIMARY if is_selected else ft.Colors.ON_SURFACE_VARIANT
        self._icon_control.color = color
        self._text_control.color = color
        if self.page:
            self.update()
