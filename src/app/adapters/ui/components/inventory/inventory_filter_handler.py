from uuid import UUID

from app.application.inventory.search_service import InventorySearchService
from app.domain.inventory.inventory_item import InventoryItem


class InventoryFilterHandler:
    """Encapsulates search logic for inventory."""

    def __init__(self, search_service: InventorySearchService) -> None:
        self._search_service = search_service

    def filter(self, query: str | None = None) -> list[InventoryItem]:
        clean_query = (query or "").strip()
        if not clean_query:
            return self._search_service.get_all()
        return self._filter_by_query(clean_query)

    def _filter_by_query(self, query: str) -> list[InventoryItem]:
        try:
            parsed_id = UUID(query)
            inventory_item_by_id = self._search_service.get_by_id(parsed_id)
            return [inventory_item_by_id] if inventory_item_by_id else []
        except ValueError:
            pass
        inventory_item_by_name = self._search_service.get_by_name(query)
        return [inventory_item_by_name] if inventory_item_by_name else []
