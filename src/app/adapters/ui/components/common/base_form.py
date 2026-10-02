from abc import ABC, abstractmethod
from collections.abc import Callable

import flet as ft

from app.adapters.ui.components.common.controls import (
    create_close_button,
    create_divider,
    create_header,
    create_save_button,
    create_text,
)
from app.adapters.ui.theme import theme


class BaseForm[T](ft.Column, ABC):
    """Represents an abstract form component for creating and editing entities."""

    def __init__(
        self,
        title: str,
        on_save: Callable[[T], None] | None = None,
        on_close: Callable[[], None] | None = None,
        extra_header_controls: list[ft.Control] | None = None,
    ) -> None:
        super().__init__(
            spacing=theme.spacing_medium,
            scroll=ft.ScrollMode.AUTO,
            expand=True,
        )
        self._on_save = on_save
        self._on_close = on_close
        self._error_text = create_text(
            value="",
            color=theme.color_danger,
            size=theme.font_size_small,
            visible=False,
        )
        header_controls: list[ft.Control] = []
        if extra_header_controls:
            header_controls.extend(extra_header_controls)
        header_controls.append(create_save_button(on_click=self._handle_save))
        header_controls.append(
            create_close_button(on_click=lambda _: self._on_close and self._on_close())
        )
        header_row = ft.Row(
            controls=[create_header(title), ft.Row(controls=header_controls)],
            alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
        )
        form_body = self._build_form_controls()
        self.controls = [header_row, create_divider(), self._error_text, *form_body]

    @abstractmethod
    def _extract_entity(self) -> T: ...

    def _handle_save(self, e: ft.ControlEvent) -> None:
        try:
            entity = self._extract_entity()
            self._error_text.visible = False
            if self._on_save:
                self._on_save(entity)
        except (TypeError, ValueError) as err:
            self._error_text.value = str(err)
            self._error_text.visible = True
            self.update()

    @abstractmethod
    def _build_form_controls(self) -> list[ft.Control]: ...
