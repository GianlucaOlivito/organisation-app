import flet as ft


def test_info_view_initialization(info_view):
    assert info_view is not None
    assert len(info_view.controls) == 3
    assert info_view.controls[0].value == "Info"


def test_info_view_renders_metadata_rows(info_view):
    container = info_view.controls[2]
    content_row = container.content

    assert isinstance(content_row, ft.Row)
    assert len(content_row.controls) == 3
