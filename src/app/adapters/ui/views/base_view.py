from abc import ABC, abstractmethod

import flet as ft


class BaseView(ft.Column, ABC):
    """Represents an abstract base layout for all application views."""

    def __init__(self, title: str) -> None:
        super().__init__(expand=True, spacing=20)
        self.controls = [
            ft.Text(title, size=28, weight=ft.FontWeight.BOLD),
            ft.Divider(),
        ]
        self._build_view()

    @abstractmethod
    def _build_view(self) -> None: ...
