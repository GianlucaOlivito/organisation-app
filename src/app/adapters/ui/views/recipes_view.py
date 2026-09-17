import flet as ft

from .base_view import BaseView


class RecipesView(BaseView):
    """Represents a view component for recipe management."""

    def __init__(self) -> None:
        super().__init__(title="Recipe Management")

    def _build_view(self) -> None:
        self.controls.append(ft.Text("Recipe management is being implemented..."))
