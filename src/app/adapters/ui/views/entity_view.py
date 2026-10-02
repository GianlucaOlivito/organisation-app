from abc import abstractmethod

import flet as ft

from app.adapters.ui.components.common.controls import (
    create_container,
    create_muted_text,
)

from .base_view import BaseView


class EntityView[T](BaseView):
    """Represents an abstract view component for views of domain entities."""

    def __init__(self, title: str, empty_text: str) -> None:
        self._empty_state = create_container(
            content=create_muted_text(empty_text),
            alignment=ft.Alignment.CENTER,
            expand=True,
        )
        self._content_container = ft.Column(
            expand=True,
            alignment=ft.MainAxisAlignment.START,
            horizontal_alignment=ft.CrossAxisAlignment.STRETCH,
            controls=[self._empty_state],
        )
        self._toolbar = self._build_toolbar()
        super().__init__(title=title)
        self._search()

    @abstractmethod
    def _build_toolbar(self) -> ft.Row: ...

    @abstractmethod
    def _search(self, e: ft.ControlEvent | None = None) -> None: ...

    @abstractmethod
    def _create_form(
        self,
        entity: T | None,
        on_save: callable,
        on_close: callable,
    ) -> ft.Control: ...

    @abstractmethod
    def _save_entity(self, entity: T, is_edit: bool) -> None: ...

    def _close_form(self) -> None:
        self._toolbar.visible = True
        self._search()

    def _open_form(self, entity: T | None = None) -> None:
        def _handle_save(saved_entity: T) -> None:
            self._save_entity(saved_entity, is_edit=entity is not None)
            self._close_form()

        self._toolbar.visible = False
        self._content_container.controls = [
            self._create_form(
                entity=entity,
                on_save=_handle_save,
                on_close=self._close_form,
            )
        ]
        self.update()

    def _build_view(self) -> None:
        self.controls.extend([self._toolbar, self._content_container])
