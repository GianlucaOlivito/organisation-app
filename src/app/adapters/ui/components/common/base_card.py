from abc import ABC, abstractmethod
from collections.abc import Callable
from uuid import UUID

import flet as ft

from app.adapters.ui.components.common.controls import (
    create_container,
    create_delete_button,
    create_edit_button,
    create_muted_text,
    create_text,
)
from app.adapters.ui.theme import theme


class BaseCard[T](ft.Card, ABC):
    """Represents an abstract component to display entities."""

    def __init__(
        self,
        entity: T,
        on_edit: Callable[[T], None] | None = None,
        on_delete: Callable[[UUID], None] | None = None,
    ) -> None:
        self.entity = entity
        self.on_edit = on_edit
        self.on_delete = on_delete
        super().__init__(
            expand=True,
            content=create_container(
                content=ft.Column(
                    controls=self._build_card_content(),
                    spacing=theme.spacing_medium,
                    scroll=ft.ScrollMode.AUTO,
                    expand=True,
                )
            ),
        )

    def _build_header(self, title: str, entity_id: UUID | None = None) -> ft.Control:
        action_controls: list[ft.Control] = []
        if self.on_edit:
            action_controls.append(
                create_edit_button(on_click=lambda _: self.on_edit(self.entity))
            )
        if self.on_delete and entity_id:
            action_controls.append(
                create_delete_button(on_click=lambda _: self.on_delete(entity_id))
            )
        header_right_controls: list[ft.Control] = []
        if entity_id:
            header_right_controls.append(create_muted_text(f"ID: {str(entity_id)[:8]}"))
        header_right_controls.extend(action_controls)
        return ft.Row(
            controls=[
                create_text(title, weight=theme.font_weight_semibold, expand=True),
                ft.Row(
                    controls=header_right_controls,
                    spacing=theme.spacing_small,
                    vertical_alignment=ft.CrossAxisAlignment.CENTER,
                ),
            ],
            alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
        )

    @abstractmethod
    def _build_card_content(self) -> list[ft.Control]: ...
