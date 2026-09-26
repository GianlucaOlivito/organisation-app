from dataclasses import dataclass, field
from typing import Any

import flet as ft


@dataclass(frozen=True, slots=True)
class Theme:
    """Utility class for UI theme tokens and styling constants."""

    page_theme_mode: ft.ThemeMode = ft.ThemeMode.SYSTEM
    spacing_none: int = 0
    spacing_small: int = 4
    spacing_medium: int = 10
    spacing_large: int = 20
    divider_width: int = 1
    border_radius_medium: int = 8
    sidebar_width: int = 100
    container_height_medium: int = 200
    grid_max_extent: int = 400
    grid_aspect_ratio: float = 1.0
    input_field_min_lines: int = 5
    input_field_max_lines: int = 10
    font_family: str = "Consolas"
    font_size_xl: int = 24
    font_size_large: int = 20
    font_size_medium: int = 16
    font_size_small: int = 12
    font_weight_bold: str = ft.FontWeight.BOLD
    font_weight_semibold: str = ft.FontWeight.W_600
    color_danger: str = ft.Colors.RED_300
    color_active: str = ft.Colors.PRIMARY
    color_inactive: str = ft.Colors.ON_SURFACE_VARIANT
    color_text_muted: str = ft.Colors.GREY_600
    color_bg: str = ft.Colors.GREY_900
    colors_log_levels: dict[str, dict[str, Any]] = field(
        default_factory=lambda: {
            "DEBUG": {"color": "#ADD8E6", "bgcolor": None},
            "INFO": {"color": "#74E3A8", "bgcolor": None},
            "WARNING": {"color": "#F5B742", "bgcolor": None},
            "ERROR": {"color": "#E55A5A", "bgcolor": None},
            "CRITICAL": {"color": "#FFFFFF", "bgcolor": "#C93737"},
        }
    )


theme = Theme()
