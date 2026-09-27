from unittest.mock import MagicMock

import flet as ft

from app.adapters.ui.components.common.sidebar import Sidebar
from app.adapters.ui.theme import theme


def test_sidebar_initialization():
    items = [(ft.Icons.HOME, "Home"), (ft.Icons.SETTINGS, "Settings")]
    sidebar = Sidebar(items=items, selected_index=0)

    assert len(sidebar.controls) == 2
    assert sidebar._selected_index == 0

    active_icon, active_text = sidebar._tab_refs[0]

    assert active_icon.color == theme.color_active
    assert active_text.color == theme.color_active

    inactive_icon, inactive_text = sidebar._tab_refs[1]

    assert inactive_icon.color == theme.color_inactive
    assert inactive_text.color == theme.color_inactive


def test_sidebar_tab_selection_updates_colors_and_triggers_callback():
    on_change_mock = MagicMock()
    items = [(ft.Icons.HOME, "Home"), (ft.Icons.SETTINGS, "Settings")]
    sidebar = Sidebar(items=items, selected_index=0, on_change=on_change_mock)
    sidebar.update = MagicMock()
    sidebar._handle_select(1)

    assert sidebar._selected_index == 1

    old_icon, old_text = sidebar._tab_refs[0]

    assert old_icon.color == theme.color_inactive
    assert old_text.color == theme.color_inactive

    new_icon, new_text = sidebar._tab_refs[1]

    assert new_icon.color == theme.color_active
    assert new_text.color == theme.color_active
    sidebar.update.assert_called_once()
    on_change_mock.assert_called_once_with(1)


def test_sidebar_selecting_current_tab_is_noop():
    on_change_mock = MagicMock()
    items = [(ft.Icons.HOME, "Home"), (ft.Icons.SETTINGS, "Settings")]
    sidebar = Sidebar(items=items, selected_index=0, on_change=on_change_mock)
    sidebar.update = MagicMock()
    sidebar._handle_select(0)

    assert sidebar._selected_index == 0
    sidebar.update.assert_not_called()
    on_change_mock.assert_not_called()
