import asyncio
from unittest.mock import MagicMock

import flet as ft
import pytest

from app.adapters.ui.theme import theme


def test_initialization(logs_view):
    assert logs_view._enabled_levels == set(theme.log_levels)
    assert isinstance(logs_view._logs, ft.ListView)
    assert isinstance(logs_view._filter, ft.SegmentedButton)
    assert logs_view._loop is None


def test_build_log_line(logs_view):
    text_control = logs_view._build_log_line("ERROR", "Something broke")

    assert isinstance(text_control, ft.Text)
    assert text_control.value == "Something broke"
    assert text_control.color == theme.colors_log_levels["ERROR"]["color"]

    fallback_control = logs_view._build_log_line("UNKNOWN", "Test message")

    assert fallback_control.color == theme.colors_log_levels["INFO"]["color"]


def test_build_view(logs_view):
    assert len(logs_view.controls) == 4
    assert isinstance(logs_view.controls[0], ft.Text)
    assert isinstance(logs_view.controls[1], ft.Divider)
    assert isinstance(logs_view.controls[2], ft.Row)
    assert isinstance(logs_view.controls[3], ft.Container)


def test_render_filters_disabled_levels(log_buffer, logs_view):
    log_buffer.append("INFO", "Info message")
    log_buffer.append("DEBUG", "Debug message")
    logs_view._enabled_levels = {"INFO"}
    logs_view._render()

    assert len(logs_view._logs.controls) == 1
    assert logs_view._logs.controls[0].value == "Info message"


def test_clear_logs_button_action(log_buffer, logs_view):
    log_buffer.append("INFO", "Log to clear")
    assert len(log_buffer.take_snapshot()) == 1

    clear_button = logs_view.controls[2].controls[1]
    clear_button.on_click(None)

    assert len(log_buffer.take_snapshot()) == 0


def test_filter_logs_event(logs_view):
    mock_event = MagicMock()
    mock_event.control.selected = ["ERROR", "CRITICAL"]
    logs_view._filter.on_change(mock_event)

    assert logs_view._enabled_levels == {"ERROR", "CRITICAL"}


@pytest.mark.asyncio
async def test_lifecycle_hooks(log_buffer, logs_view):
    logs_view.did_mount()

    assert logs_view._loop is not None
    assert logs_view._update_from_buffer in log_buffer._listeners

    logs_view.will_unmount()

    assert logs_view._loop is None
    assert logs_view._update_from_buffer not in log_buffer._listeners


def test_update_from_buffer_threadsafe(logs_view):
    mock_loop = MagicMock(spec=asyncio.AbstractEventLoop)
    mock_loop.is_running.return_value = True
    logs_view._loop = mock_loop
    logs_view._update_from_buffer()

    mock_loop.call_soon_threadsafe.assert_called_once_with(logs_view._render)
