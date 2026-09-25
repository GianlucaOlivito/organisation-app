import flet as ft

from app.adapters.ui.components.common.controls import (
    create_container,
    create_delete_button,
    create_divider,
    create_filter_button,
    create_header,
    create_icon_button,
    create_muted_text,
    create_search_button,
    create_text,
    create_text_field,
    create_title,
    create_vertical_divider,
)
from app.adapters.ui.theme import theme


def test_create_title():
    title = create_title("Test Title")

    assert isinstance(title, ft.Text)
    assert title.value == "Test Title"
    assert title.size == theme.font_size_xl
    assert title.weight == theme.font_weight_bold
    assert title.font_family == theme.font_family

    custom_title = create_title("Custom Title", size=30, color=ft.Colors.RED)

    assert custom_title.size == 30
    assert custom_title.color == ft.Colors.RED


def test_create_header():
    header = create_header("Test Header")

    assert isinstance(header, ft.Text)
    assert header.value == "Test Header"
    assert header.size == theme.font_size_large
    assert header.weight == theme.font_weight_semibold
    assert header.font_family == theme.font_family


def test_create_text():
    text = create_text("Test Text")

    assert isinstance(text, ft.Text)
    assert text.value == "Test Text"
    assert text.size == theme.font_size_medium
    assert text.font_family == theme.font_family


def test_create_muted_text():
    muted = create_muted_text("Muted Text")

    assert isinstance(muted, ft.Text)
    assert muted.value == "Muted Text"
    assert muted.size == theme.font_size_small
    assert muted.italic is True
    assert muted.color == theme.color_text_muted
    assert muted.font_family == theme.font_family


def test_create_text_field():
    field = create_text_field("Enter text...")

    assert isinstance(field, ft.TextField)
    assert field.hint_text == "Enter text..."
    assert field.bgcolor == theme.color_bg
    assert field.border_radius == theme.border_radius_medium
    assert field.expand is True
    assert field.dense is True
    assert field.text_style.font_family == theme.font_family
    assert field.hint_style.italic is True
    assert field.hint_style.color == theme.color_text_muted

    custom_field = create_text_field("Search", expand=False, dense=False)

    assert custom_field.expand is False
    assert custom_field.dense is False


def test_create_icon_button():
    btn = create_icon_button(ft.Icons.ADD)

    assert isinstance(btn, ft.IconButton)
    assert btn.icon == ft.Icons.ADD
    assert btn.icon_color == theme.color_inactive


def test_create_search_button():
    btn = create_search_button()

    assert isinstance(btn, ft.IconButton)
    assert btn.icon == ft.Icons.SEARCH
    assert btn.icon_color == theme.color_active


def test_create_filter_button():
    btn = create_filter_button()

    assert isinstance(btn, ft.IconButton)
    assert btn.icon == ft.Icons.FILTER_ALT
    assert btn.icon_color == theme.color_active


def test_create_delete_button():
    btn = create_delete_button()

    assert isinstance(btn, ft.IconButton)
    assert btn.icon == ft.Icons.DELETE_SWEEP
    assert btn.icon_color == theme.color_danger


def test_create_dividers():
    divider = create_divider()

    assert isinstance(divider, ft.Divider)
    assert divider.height == theme.divider_width

    v_divider = create_vertical_divider()

    assert isinstance(v_divider, ft.VerticalDivider)
    assert v_divider.width == theme.divider_width


def test_create_container():
    container = create_container()

    assert isinstance(container, ft.Container)
    assert container.padding == theme.spacing_large
    assert container.border_radius == theme.border_radius_medium

    text = create_text("Inside Container")
    custom_container = create_container(content=text, padding=theme.spacing_small)

    assert custom_container.content == text
    assert custom_container.padding == theme.spacing_small
