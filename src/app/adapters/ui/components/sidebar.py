from collections.abc import Callable
from dataclasses import dataclass

import flet as ft

from .navigation_tab import NavigationTab


@dataclass(frozen=True, slots=True)
class NavigationItemConfig:
    """Represents configuration data for sidebar navigation items."""

    icon: str
    label: str


class Sidebar(ft.Column):
    """Represents sidebar navigation container managing tabs and selection state."""

    def __init__(
        self,
        items: list[NavigationItemConfig],
        selected_index: int = 0,
        on_change: Callable[[int], None] | None = None,
    ) -> None:
        self._items = items
        self._selected_index = selected_index
        self._on_change = on_change
        self._tabs: list[NavigationTab] = [
            NavigationTab(
                index=i,
                icon=item.icon,
                label=item.label,
                is_selected=(i == selected_index),
                on_select=self._handle_select,
            )
            for i, item in enumerate(items)
        ]
        super().__init__(
            alignment=ft.MainAxisAlignment.SPACE_EVENLY,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            width=100,
            controls=self._tabs,
        )

    def _handle_select(self, index: int) -> None:
        if index == self._selected_index:
            return
        self._tabs[self._selected_index].set_active(False)
        self._tabs[index].set_active(True)
        self._selected_index = index
        if self._on_change:
            self._on_change(index)
