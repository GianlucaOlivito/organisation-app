from datetime import date

from app.adapters.ui.components.common.filter_helpers import parse_str_to_date
from app.application.inventory.shopping_list_service import ShoppingListService
from app.domain.inventory.shopping_list import ShoppingList


class ShoppingListFilterHandler:
    """Encapsulates filter rules and search logic for shopping lists."""

    def __init__(self, shopping_list_service: ShoppingListService) -> None:
        self._shopping_list_service = shopping_list_service

    def filter(
        self,
        start_date: date | str | None = None,
        end_date: date | str | None = None,
    ) -> ShoppingList | None:
        parsed_start = parse_str_to_date(start_date)
        parsed_end = parse_str_to_date(end_date)
        if not parsed_start or not parsed_end or parsed_start > parsed_end:
            return None
        try:
            return self._shopping_list_service.generate_shopping_list(
                parsed_start, parsed_end
            )
        except ValueError:
            return None
