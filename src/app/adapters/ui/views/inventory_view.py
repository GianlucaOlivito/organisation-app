import flet as ft

from .base_view import BaseView


class InventoryView(BaseView):
    """Represents a view component for inventory management."""

    def __init__(self) -> None:
        super().__init__(title="Inventory Management")

    def _build_view(self) -> None:
        self.controls.append(ft.Text("Inventory management is being implemented..."))
