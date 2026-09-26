import flet as ft

from app.adapters.ui.theme import theme


def create_title(value: str, **kwargs) -> ft.Text:
    kwargs.setdefault("size", theme.font_size_xl)
    kwargs.setdefault("weight", theme.font_weight_bold)
    kwargs.setdefault("font_family", theme.font_family)
    return ft.Text(value=value, **kwargs)


def create_header(value: str, **kwargs) -> ft.Text:
    kwargs.setdefault("size", theme.font_size_large)
    kwargs.setdefault("weight", theme.font_weight_semibold)
    kwargs.setdefault("font_family", theme.font_family)
    return ft.Text(value=value, **kwargs)


def create_text(value: str, **kwargs) -> ft.Text:
    kwargs.setdefault("size", theme.font_size_medium)
    kwargs.setdefault("font_family", theme.font_family)
    return ft.Text(value=value, **kwargs)


def create_muted_text(value: str, **kwargs) -> ft.Text:
    kwargs.setdefault("size", theme.font_size_small)
    kwargs.setdefault("italic", True)
    kwargs.setdefault("color", theme.color_text_muted)
    return create_text(value=value, **kwargs)


def create_text_field(hint_text: str, **kwargs) -> ft.TextField:
    kwargs.setdefault("hint_text", hint_text)
    kwargs.setdefault("text_style", ft.TextStyle(font_family=theme.font_family))
    kwargs.setdefault("bgcolor", theme.color_bg)
    kwargs.setdefault("border_radius", theme.border_radius_medium)
    kwargs.setdefault("expand", True)
    kwargs.setdefault("dense", True)
    kwargs.setdefault(
        "hint_style",
        ft.TextStyle(
            italic=True,
            color=theme.color_text_muted,
            font_family=theme.font_family,
        ),
    )
    return ft.TextField(**kwargs)


def create_icon_button(icon: str, **kwargs) -> ft.IconButton:
    kwargs.setdefault("icon_color", theme.color_inactive)
    return ft.IconButton(icon=icon, **kwargs)


def create_search_button(**kwargs) -> ft.IconButton:
    kwargs.setdefault("icon_color", theme.color_active)
    return create_icon_button(icon=ft.Icons.SEARCH, **kwargs)


def create_filter_button(**kwargs) -> ft.IconButton:
    kwargs.setdefault("icon_color", theme.color_active)
    return create_icon_button(icon=ft.Icons.FILTER_ALT, **kwargs)


def create_add_button(**kwargs) -> ft.IconButton:
    kwargs.setdefault("icon_color", theme.color_active)
    return create_icon_button(icon=ft.Icons.ADD, **kwargs)


def create_edit_button(**kwargs) -> ft.IconButton:
    kwargs.setdefault("icon_color", theme.color_active)
    return create_icon_button(icon=ft.Icons.EDIT, **kwargs)


def create_save_button(**kwargs) -> ft.IconButton:
    kwargs.setdefault("icon_color", theme.color_active)
    return create_icon_button(icon=ft.Icons.SAVE, **kwargs)


def create_close_button(**kwargs) -> ft.IconButton:
    return create_icon_button(icon=ft.Icons.CLOSE, **kwargs)


def create_delete_button(**kwargs) -> ft.IconButton:
    kwargs.setdefault("icon_color", theme.color_danger)
    return create_icon_button(icon=ft.Icons.DELETE_SWEEP, **kwargs)


def create_divider(**kwargs) -> ft.Divider:
    kwargs.setdefault("height", theme.divider_width)
    return ft.Divider(**kwargs)


def create_vertical_divider(**kwargs) -> ft.VerticalDivider:
    kwargs.setdefault("width", theme.divider_width)
    return ft.VerticalDivider(**kwargs)


def create_container(**kwargs) -> ft.Container:
    kwargs.setdefault("padding", theme.spacing_large)
    kwargs.setdefault("border_radius", theme.border_radius_medium)
    return ft.Container(**kwargs)
