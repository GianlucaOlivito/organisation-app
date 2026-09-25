import asyncio
from typing import Any

import flet as ft

from app.adapters.ui.components.common.controls import (
    create_container,
    create_delete_button,
    create_text,
)
from app.adapters.ui.theme import theme
from app.infrastructure.log_buffer import LogBuffer

from .base_view import BaseView


class LogsView(BaseView):
    """Represents a view component for logs."""

    LEVELS: tuple[str, ...] = ("DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL")

    def __init__(self, log_buffer: LogBuffer) -> None:
        self._log_buffer = log_buffer
        self._enabled_levels = set(self.LEVELS)
        self._loop = None
        self._logs = ft.ListView(
            expand=True, spacing=theme.spacing_small, auto_scroll=True
        )
        self._filter = self._create_level_filter()
        super().__init__(title="Logs")

    def _build_log_line(self, level: str, message: str) -> ft.Text:
        style = theme.colors_log_levels.get(level, theme.colors_log_levels["INFO"])
        return create_text(
            message,
            size=theme.font_size_small,
            selectable=True,
            color=style["color"],
            bgcolor=style["bgcolor"],
        )

    def _render(self) -> None:
        entries = self._log_buffer.take_snapshot()
        self._logs.controls = [
            self._build_log_line(level, message)
            for level, message in entries
            if level in self._enabled_levels
        ]
        try:
            if self._logs.page:
                self._logs.update()
        except RuntimeError:
            pass

    def _update_from_buffer(self) -> None:
        if self._loop is not None and self._loop.is_running():
            self._loop.call_soon_threadsafe(self._render)

    def did_mount(self) -> None:
        self._loop = asyncio.get_running_loop()
        self._log_buffer.subscribe(self._update_from_buffer)
        self._render()

    def will_unmount(self) -> None:
        self._log_buffer.unsubscribe(self._update_from_buffer)
        self._loop = None

    def _filter_logs(self, e: Any) -> None:
        self._enabled_levels = set(e.control.selected)
        self._render()

    def _create_level_filter(self) -> ft.SegmentedButton:
        return ft.SegmentedButton(
            segments=[
                ft.Segment(
                    value=level, label=create_text(level, size=theme.font_size_small)
                )
                for level in self.LEVELS
            ],
            selected=list(self.LEVELS),
            allow_multiple_selection=True,
            allow_empty_selection=True,
            on_change=self._filter_logs,
        )

    def _build_view(self) -> None:
        toolbar = ft.Row(
            controls=[
                self._filter,
                create_delete_button(
                    tooltip="Clear logs",
                    on_click=lambda _: self._log_buffer.clear(),
                ),
            ],
            alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
        )
        log_container = create_container(
            content=self._logs, bgcolor=theme.color_bg, expand=True
        )
        self.controls.extend([toolbar, log_container])
