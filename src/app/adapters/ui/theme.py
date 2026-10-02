from dataclasses import dataclass, field

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
    grid_max_extent: int = 400
    grid_aspect_ratio: float = 1.0
    col_width_small: int = 100
    input_field_min_lines: int = 5
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
    colors_log_levels: dict[str, dict[str, str | None]] = field(
        default_factory=lambda: {
            "DEBUG": {"color": "#ADD8E6", "bgcolor": None},
            "INFO": {"color": "#74E3A8", "bgcolor": None},
            "WARNING": {"color": "#F5B742", "bgcolor": None},
            "ERROR": {"color": "#E55A5A", "bgcolor": None},
            "CRITICAL": {"color": "#FFFFFF", "bgcolor": "#C93737"},
        }
    )
    scrollbar_theme: ft.ScrollbarTheme = field(
        default_factory=lambda: ft.ScrollbarTheme(
            thumb_visibility=False,
            track_visibility=False,
            thickness=6,
            radius=3,
            thumb_color={
                ft.ControlState.DEFAULT: ft.Colors.WHITE_24,
                ft.ControlState.HOVERED: ft.Colors.PRIMARY,
                ft.ControlState.DRAGGED: ft.Colors.PRIMARY,
            },
            main_axis_margin=4,
        )
    )

    @property
    def log_levels(self) -> tuple[str, ...]:
        return tuple(self.colors_log_levels.keys())


theme = Theme()
