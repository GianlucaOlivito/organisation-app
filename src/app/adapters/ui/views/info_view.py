import flet as ft

from app.adapters.ui.components.common.controls import (
    create_container,
    create_header,
    create_muted_text,
    create_vertical_divider,
)
from app.adapters.ui.theme import theme
from app.config.settings import Settings

from .base_view import BaseView


class InfoView(BaseView):
    """Represents a view component for app metadata info."""

    def __init__(self, settings: Settings) -> None:
        self._settings = settings
        self._info = {
            "Product Title": self._settings.app_title,
            "Product Version": self._settings.app_version,
            "Product Owner": "Gianluca Olivito",
            "Product Developer": "Gianluca Olivito",
            "Language": "Python 3.14",
            "UI Framework": "Flet 0.86.5",
        }
        super().__init__(title="Info")

    def _build_rows(self) -> list[ft.Control]:
        rows: list[ft.Control] = []
        for key, value in self._info.items():
            row = ft.Row(
                controls=[
                    create_header(
                        f"{key}", color=theme.color_active, width=theme.col_width_medium
                    ),
                    create_muted_text(f"{value}", size=theme.font_size_large),
                ],
                alignment=ft.MainAxisAlignment.START,
                vertical_alignment=ft.CrossAxisAlignment.CENTER,
            )
            rows.append(row)
        return rows

    def _build_info(self) -> ft.Control:
        return create_container(
            content=ft.Column(
                controls=self._build_rows(),
                spacing=theme.spacing_medium,
                alignment=ft.MainAxisAlignment.CENTER,
            ),
            expand=True,
        )

    def _build_logo(self) -> ft.Control:
        return create_container(
            content=ft.Column(
                controls=ft.Image(src=self._settings.app_logo_png),
                spacing=theme.spacing_medium,
                alignment=ft.MainAxisAlignment.CENTER,
            ),
            expand=True,
        )

    def _build_view(self) -> None:
        content_row = ft.Row(
            controls=[
                self._build_info(),
                create_vertical_divider(),
                self._build_logo(),
            ],
            alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
            vertical_alignment=ft.CrossAxisAlignment.CENTER,
            expand=True,
        )
        self.controls.extend([create_container(content=content_row, expand=True)])
