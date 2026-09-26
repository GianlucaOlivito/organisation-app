from datetime import date
from pathlib import Path
from typing import Any
from uuid import UUID

from app.adapters.common.json_base_repository import JsonBaseRepository
from app.application.meal_planning.repository import MenuRepository
from app.config.settings import settings
from app.domain.meal_planning.course import Course
from app.domain.meal_planning.menu import Menu


class JsonMenuRepository(JsonBaseRepository[Menu], MenuRepository):
    """Implementation part of UC-2.1 and UC-2.2: Manage menus persistence with JSON."""

    def __init__(self, file_path: Path | None = None) -> None:
        super().__init__(file_path=file_path or settings.menus_file_path)

    def _entity_to_dict(self, menu: Menu) -> dict[str, Any]:
        return {
            "id": str(menu.id),
            "description": menu.description,
            "scheduled_date": menu.scheduled_date.isoformat(),
            "courses": [
                {
                    "recipe_id": str(course.recipe_id),
                    "portions": course.portions,
                }
                for course in menu.courses
            ],
        }

    def _dict_to_entity(self, data: dict[str, Any]) -> Menu:
        courses = [
            Course(
                recipe_id=UUID(course_data["recipe_id"]),
                portions=course_data["portions"],
            )
            for course_data in data.get("courses", [])
        ]
        return Menu(
            id=UUID(data["id"]),
            description=data["description"],
            scheduled_date=date.fromisoformat(data["scheduled_date"]),
            courses=courses,
        )

    def filter_by_date_range(self, start_date: date, end_date: date) -> list[Menu]:
        matching_menus: list[Menu] = []
        for menu in self.get_all():
            if start_date <= menu.scheduled_date <= end_date:
                matching_menus.append(menu)
        return matching_menus
