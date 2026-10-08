import logging
from collections import defaultdict
from datetime import date

from app.application.common.calculators import (
    calculate_menu_ingredients,
    standardize_unit,
)
from app.application.common.validators import validate_date_range
from app.application.meal_planning.search_service import MenuSearchService
from app.application.recipes.search_service import RecipeSearchService
from app.domain.inventory.shopping_list import ShoppingList
from app.domain.inventory.shopping_list_item import ShoppingListItem

from .search_service import InventorySearchService

logger = logging.getLogger(__name__)


class ShoppingListService:
    """Service for use case UC-3.3: Generate Shopping List."""

    def __init__(
        self,
        recipe_search_service: RecipeSearchService,
        menu_search_service: MenuSearchService,
        inventory_search_service: InventorySearchService,
    ) -> None:
        self._recipe_search_service = recipe_search_service
        self._menu_search_service = menu_search_service
        self._inventory_search_service = inventory_search_service
        logger.debug("Initialized %s.", self.__class__.__name__)

    def generate_shopping_list(self, start_date: date, end_date: date) -> ShoppingList:
        validate_date_range(start_date, end_date)
        menus = self._menu_search_service.filter_by_date_range(start_date, end_date)
        needed_totals = calculate_menu_ingredients(menus, self._recipe_search_service)
        inventory_items = self._inventory_search_service.get_all()
        available_totals: dict[tuple[str, str], float] = defaultdict(float)
        for item in inventory_items:
            std_qty, std_unit = standardize_unit(item.quantity, item.unit)
            key = (item.name, std_unit)
            available_totals[key] += std_qty
        shopping_items: list[ShoppingListItem] = []
        for (name, unit), required_qty in needed_totals.items():
            available_qty = available_totals.get((name, unit), 0.0)
            needed_qty = required_qty - available_qty
            if needed_qty > 0:
                shopping_items.append(
                    ShoppingListItem(name=name, quantity=needed_qty, unit=unit)
                )
        if shopping_items:
            logger.info(
                "Generated shopping list with %d item(s) for period '%s' to '%s'.",
                len(shopping_items),
                start_date,
                end_date,
            )
        else:
            logger.warning(
                "No shopping list items were required for period '%s' to '%s'.",
                start_date,
                end_date,
            )
        return ShoppingList(items=shopping_items)
