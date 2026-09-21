import asyncio
from typing import Any, ClassVar

import flet as ft

from app.infrastructure.log_buffer import LogBuffer

from .base_view import BaseView


class LogsView(BaseView):
    """Represents a view component for logs."""

    LEVELS: tuple[str, ...] = ("DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL")
    LEVEL_STYLES: ClassVar[dict[str, dict[str, Any]]] = {
        "DEBUG": {"color": "#ADD8E6", "bgcolor": None},
        "INFO": {"color": "#74E3A8", "bgcolor": None},
        "WARNING": {"color": "#F5B742", "bgcolor": None},
        "ERROR": {"color": "#E55A5A", "bgcolor": None},
        "CRITICAL": {"color": "#FFFFFF", "bgcolor": "#C93737"},
    }

    def __init__(self, log_buffer: LogBuffer) -> None:
        self._log_buffer = log_buffer
        self._enabled_levels = set(self.LEVELS)
        self._loop = None
        self._logs = ft.ListView(expand=True, spacing=4, auto_scroll=True)
        self._filter = self._create_level_filter()
        super().__init__(title="Logs")

    def _build_log_line(self, level: str, message: str) -> ft.Text:
        style = self.LEVEL_STYLES.get(level, self.LEVEL_STYLES["INFO"])
        return ft.Text(
            value=message,
            selectable=True,
            font_family="Consolas",
            size=12,
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
                ft.Segment(value=level, label=ft.Text(level)) for level in self.LEVELS
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
                ft.IconButton(
                    icon=ft.Icons.DELETE_SWEEP,
                    icon_color=ft.Colors.RED_300,
                    tooltip="Clear logs",
                    on_click=lambda _: self._log_buffer.clear(),
                ),
            ],
            alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
        )
        log_container = ft.Container(
            content=self._logs,
            padding=16,
            bgcolor="#121212",
            border_radius=8,
            expand=True,
        )
        self.controls.extend([toolbar, log_container])
