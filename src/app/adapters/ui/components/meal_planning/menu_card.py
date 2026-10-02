from collections.abc import Callable
from uuid import UUID

import flet as ft

from app.adapters.ui.components.common.base_card import BaseCard
from app.adapters.ui.components.common.controls import create_divider, create_text
from app.adapters.ui.theme import theme
from app.application.recipes.search_service import RecipeSearchService
from app.domain.meal_planning.menu import Menu


class MenuCard(BaseCard[Menu]):
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
        super().__init__(entity=menu, on_edit=on_edit, on_delete=on_delete)

    @staticmethod
    def _format_course(portions: int, course_name: str) -> str:
        portion_str = "Portion" if portions == 1 else "Portionen"
        return f"• {portions} {portion_str} {course_name}"

    def _build_courses_section(self) -> ft.Control:
        courses_controls = []
        for course in self.menu.courses:
            recipe = self.recipe_search_service.get_by_id(course.recipe_id)
            course_name = recipe.name if recipe else "Unbekanntes Rezept"
            courses_controls.append(
                create_text(self._format_course(course.portions, course_name))
            )
        return ft.Column(
            controls=[create_text("Gänge"), *courses_controls],
            spacing=theme.spacing_small,
        )

    def _build_card_content(self) -> list[ft.Control]:
        formatted_date = self.menu.scheduled_date.strftime("%d.%m.%Y")
        header_text = f"{self.menu.description.strip()}, {formatted_date}"
        return [
            self._build_header(title=header_text, entity_id=self.menu.id),
            create_divider(),
            self._build_courses_section(),
        ]
