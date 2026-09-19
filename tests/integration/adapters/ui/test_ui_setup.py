from unittest.mock import AsyncMock, MagicMock

import flet as ft
import pytest

from app.adapters.ui.app import App
from app.adapters.ui.layout import AppLayout
from app.infrastructure.container import create_container


@pytest.mark.asyncio
async def test_app_initialization_configures_page_settings():
    container = create_container()
    app = App(container=container)
    page = MagicMock(spec=ft.Page)
    page.window = MagicMock()
    page.window.center = AsyncMock()
    await app(page)
    cfg = container.settings

    assert page.title == cfg.app_title
    assert page.window.icon == str(cfg.assets_dir / cfg.app_logo_file_name)
    assert page.theme_mode == ft.ThemeMode.SYSTEM
    assert page.padding == 0
    assert page.window.width == cfg.window_width
    assert page.window.height == cfg.window_height
    assert page.window.min_width == cfg.window_min_width
    assert page.window.min_height == cfg.window_min_height

    page.window.center.assert_awaited_once()
    page.add.assert_called_once()
    added_control = page.add.call_args[0][0]

    assert isinstance(added_control, AppLayout)
    page.update.assert_called_once()
