import logging
from datetime import date
from pathlib import Path
from typing import Any
from uuid import UUID

from app.adapters.common.json_file_handler import read_json_file, write_json_file
from app.application.meal_planning.repository import MenuRepository
from app.config.settings import settings
from app.domain.meal_planning.course import Course
from app.domain.meal_planning.menu import Menu

logger = logging.getLogger(__name__)


class JsonMenuRepository(MenuRepository):
    """Implementation part of UC-2.1 and UC-2.2: Manage menus persistence with JSON."""

    def __init__(self, file_path: Path | None = None) -> None:
        self._file_path = file_path or settings.menus_file_path
        logger.debug("JsonMenuRepository initialized with path: %s", self._file_path)

    def _menu_to_dict(self, menu: Menu) -> dict[str, Any]:
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

    def _dict_to_menu(self, data: dict[str, Any]) -> Menu:
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

    def get_all(self) -> list[Menu]:
        raw_data = read_json_file(self._file_path)
        menus: list[Menu] = []
        for item in raw_data:
            try:
                menus.append(self._dict_to_menu(item))
            except (KeyError, ValueError, TypeError) as e:
                logger.error("Skipping invalid menu entry: %s. Error: %s", item, e)
        logger.debug("Retrieved %d menus from %s.", len(menus), self._file_path)
        return menus

    def get_by_id(self, id: UUID) -> Menu | None:
        menu = next((m for m in self.get_all() if m.id == id), None)
        if menu:
            logger.debug("Found menu with ID '%s'.", id)
        else:
            logger.debug("No menu found with ID '%s'.", id)
        return menu

    def filter_by_date_range(self, start_date: date, end_date: date) -> list[Menu]:
        matching_menus: list[Menu] = []
        for menu in self.get_all():
            if start_date <= menu.scheduled_date <= end_date:
                matching_menus.append(menu)
        logger.debug(
            "Filtered menus by date range %s to %s. Found %d matching menus.",
            start_date,
            end_date,
            len(matching_menus),
        )
        return matching_menus

    def save(self, menu: Menu) -> None:
        menus = self.get_all()
        updated = False
        for idx, existing in enumerate(menus):
            if existing.id == menu.id:
                menus[idx] = menu
                updated = True
                break
        if not updated:
            menus.append(menu)
        serialized = [self._menu_to_dict(m) for m in menus]
        write_json_file(self._file_path, serialized)
        logger.info(
            "Saved menu '%s' (description: %s) to '%s'.",
            menu.id,
            menu.description,
            self._file_path,
        )

    def delete(self, id: UUID) -> None:
        menus = self.get_all()
        filtered = [m for m in menus if m.id != id]
        if len(filtered) != len(menus):
            serialized = [self._menu_to_dict(m) for m in filtered]
            write_json_file(self._file_path, serialized)
            logger.info("Deleted menu with ID '%s' from '%s'.", id, self._file_path)
        else:
            logger.warning("Attempted to delete non-existent menu with ID '%s'.", id)
