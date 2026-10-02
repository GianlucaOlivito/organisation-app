import flet as ft

from .base_view import BaseView


class ShoppingListView(BaseView):
    """Represents a view component for shopping list management."""

    def __init__(self) -> None:
        super().__init__(title="Einkauf")

    def _build_view(self) -> None:
        self.controls.append(
            ft.Text("Shopping list management is being implemented...")
        )
