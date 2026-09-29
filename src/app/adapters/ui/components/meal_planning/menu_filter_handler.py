from datetime import date, datetime
from uuid import UUID

from app.application.meal_planning.search_service import MenuSearchService
from app.domain.meal_planning.menu import Menu


class MenuFilterHandler:
    """Encapsulates filter rules and search logic for menus."""

    def __init__(self, search_service: MenuSearchService) -> None:
        self._search_service = search_service

    def filter(
        self,
        query: str | None = None,
        start_date: date | str | None = None,
        end_date: date | str | None = None,
    ) -> list[Menu]:
        clean_query = (query or "").strip()
        parsed_start = self._parse_date(start_date)
        parsed_end = self._parse_date(end_date)
        if clean_query:
            menus = self._filter_by_query(clean_query)
        else:
            menus = self._search_service.get_all()
        if parsed_start or parsed_end:
            menus = self._filter_by_date_range(menus, parsed_start, parsed_end)
        return menus

    def _filter_by_query(self, query: str) -> list[Menu]:
        try:
            parsed_id = UUID(query)
            menu_by_id = self._search_service.get_by_id(parsed_id)
            return [menu_by_id] if menu_by_id else []
        except ValueError:
            return []

    def _filter_by_date_range(
        self,
        menus: list[Menu],
        start_date: date | None,
        end_date: date | None,
    ) -> list[Menu]:
        matching: list[Menu] = []
        for menu in menus:
            if start_date and menu.scheduled_date < start_date:
                continue
            if end_date and menu.scheduled_date > end_date:
                continue
            matching.append(menu)
        return matching

    @staticmethod
    def _parse_date(val: date | str | None) -> date | None:
        if isinstance(val, date):
            return val
        if not val or not val.strip():
            return None
        clean_val = val.strip()
        for fmt in ("%d.%m.%Y", "%Y-%m-%d"):
            try:
                return datetime.strptime(clean_val, fmt).date()  # noqa: DTZ007
            except ValueError:
                continue
        return None
