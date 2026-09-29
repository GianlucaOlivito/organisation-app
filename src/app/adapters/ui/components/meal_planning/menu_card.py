from collections.abc import Callable
from uuid import UUID

import flet as ft

from app.adapters.ui.components.common.controls import (
    create_container,
    create_delete_button,
    create_divider,
    create_edit_button,
    create_header,
    create_muted_text,
    create_text,
)
from app.adapters.ui.theme import theme
from app.application.recipes.search_service import RecipeSearchService
from app.domain.meal_planning.menu import Menu


class MenuCard(ft.Card):
    """Represents a component to display a single Menu entity."""

    def __init__(
        self,
        menu: Menu,
        recipe_search_service: RecipeSearchService,
        on_edit: Callable[[Menu], None] | None = None,
        on_delete: Callable[[UUID], None] | None = None,
    ) -> None:
        self.menu = menu
        self.recipe_search_service = recipe_search_service
        self.on_edit = on_edit
        self.on_delete = on_delete
        super().__init__(
            content=create_container(
                content=ft.Column(
                    controls=[
                        self._build_header(),
                        create_divider(),
                        self._build_courses_section(),
                    ],
                    spacing=theme.spacing_medium,
                    scroll=ft.ScrollMode.AUTO,
                    expand=True,
                ),
            )
        )

    @staticmethod
    def _format_course(portions: int, course_name: str) -> str:
        portion_str = "Portion" if portions == 1 else "Portionen"
        return f"• {portions} {portion_str} {course_name}"

    def _build_header(self) -> ft.Control:
        action_controls = []
        if self.on_edit:
            action_controls.append(
                create_edit_button(on_click=lambda _, m=self.menu: self.on_edit(m))
            )
        if self.on_delete:
            action_controls.append(
                create_delete_button(on_click=lambda _: self.on_delete(self.menu.id))
            )
        formatted_date = self.menu.scheduled_date.strftime("%d.%m.%Y")
        header_text = f"{self.menu.description.strip()}, {formatted_date}"
        return ft.Row(
            controls=[
                create_header(header_text, expand=True),
                ft.Row(
                    controls=[
                        create_muted_text(f"ID: {str(self.menu.id)[:8]}"),
                        *action_controls,
                    ],
                    spacing=theme.spacing_small,
                    vertical_alignment=ft.CrossAxisAlignment.CENTER,
                ),
            ],
            alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
        )

    def _build_courses_section(self) -> ft.Control:
        courses_controls = []
        for course in self.menu.courses:
            recipe = self.recipe_search_service.get_by_id(course.recipe_id)
            course_name = recipe.name if recipe else "Unbekanntes Rezept"
            courses_controls.append(
                create_text(
                    self._format_course(course.portions, course_name),
                    size=theme.font_size_small,
                )
            )
        return ft.Column(
            controls=[
                create_text("Gänge", weight=theme.font_weight_semibold),
                *courses_controls,
            ],
            spacing=theme.spacing_small,
        )
