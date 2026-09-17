import flet as ft

from app.infrastructure.container import Container

from .layout import AppLayout


class App:
    """Top-level UI entry point configuring page settings and app layout."""

    def __init__(self, container: Container) -> None:
        self._container = container

    async def __call__(self, page: ft.Page) -> None:
        cfg = self._container.settings
        page.title = cfg.app_title
        page.theme_mode = ft.ThemeMode.SYSTEM
        page.padding = 0
        page.window.width = cfg.window_width
        page.window.height = cfg.window_height
        page.window.min_width = cfg.window_min_width
        page.window.min_height = cfg.window_min_height
        await page.window.center()
        page.add(AppLayout())
        page.update()
