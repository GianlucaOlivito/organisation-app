import flet as ft

from app.infrastructure.container import Container

from .layout import AppLayout
from .theme import theme


class App:
    """Top-level UI entry point configuring page settings and app layout."""

    def __init__(self, container: Container) -> None:
        self._container = container

    async def _configure_page(self, page: ft.Page) -> None:
        cfg = self._container.settings
        page.title = cfg.app_title
        page.window.icon = str(cfg.assets_dir / cfg.app_logo_file_name)
        page.theme_mode = theme.page_theme_mode
        page.theme = ft.Theme(scrollbar_theme=theme.scrollbar_theme)
        page.padding = theme.spacing_none
        page.window.width = cfg.window_width
        page.window.height = cfg.window_height
        page.window.min_width = cfg.window_min_width
        page.window.min_height = cfg.window_min_height
        await page.window.center()

    async def __call__(self, page: ft.Page) -> None:
        await self._configure_page(page)
        page.add(AppLayout(self._container))
        page.update()
