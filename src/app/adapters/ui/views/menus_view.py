import flet as ft

from .base_view import BaseView


class MenusView(BaseView):
    """Represents a view component for meal planning."""

    def __init__(self) -> None:
        super().__init__(title="Meal Planning")

    def _build_view(self) -> None:
        self.controls.append(ft.Text("Meal planning is being implemented..."))
