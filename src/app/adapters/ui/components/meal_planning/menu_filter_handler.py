from datetime import date

from app.adapters.ui.components.common.filter_helpers import (
    parse_str_to_date,
    parse_str_to_uuid,
)
from app.application.meal_planning.search_service import MenuSearchService
from app.domain.meal_planning.menu import Menu


class MenuFilterHandler:
    """Encapsulates filter rules and search logic for menus."""

    def __init__(self, search_service: MenuSearchService) -> None:
        self._search_service = search_service

    def _filter_by_query(self, query: str) -> list[Menu]:
        if parsed_id := parse_str_to_uuid(query):
            menu_by_id = self._search_service.get_by_id(parsed_id)
            return [menu_by_id] if menu_by_id else []
        return []

    def filter(
        self,
        query: str | None = None,
        start_date: date | str | None = None,
        end_date: date | str | None = None,
    ) -> list[Menu]:
        clean_query = (query or "").strip()
        parsed_start = parse_str_to_date(start_date)
        parsed_end = parse_str_to_date(end_date)
        if clean_query:
            return self._filter_by_query(clean_query)
        if parsed_start or parsed_end:
            s_date = parsed_start or date.min
            e_date = parsed_end or date.max
            return self._search_service.filter_by_date_range(s_date, e_date)
        return self._search_service.get_all()
