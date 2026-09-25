from abc import ABC, abstractmethod

import flet as ft

from app.adapters.ui.components.common.controls import create_divider, create_title
from app.adapters.ui.theme import theme


class BaseView(ft.Column, ABC):
    """Represents an abstract base layout for all application views."""

    def __init__(self, title: str) -> None:
        super().__init__(expand=True, spacing=theme.spacing_large)
        self.controls = [create_title(title), create_divider()]
        self._build_view()

    @abstractmethod
    def _build_view(self) -> None: ...
