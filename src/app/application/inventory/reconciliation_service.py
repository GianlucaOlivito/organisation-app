import logging
from dataclasses import replace
from datetime import date

from app.application.common.calculators import (
    calculate_menu_ingredients,
    standardize_unit,
)
from app.application.common.validators import validate_date_range
from app.application.meal_planning.search_service import MenuSearchService
from app.application.recipes.search_service import RecipeSearchService
from app.domain.inventory.inventory_item import InventoryItem
from app.domain.inventory.shopping_list import ShoppingList

from .modification_service import InventoryModificationService
from .search_service import InventorySearchService

logger = logging.getLogger(__name__)


class InventoryReconciliationService:
    """Service for reconciling physical inventory stock with purchases and meal consumption."""

    def __init__(
        self,
        inventory_search_service: InventorySearchService,
        inventory_modification_service: InventoryModificationService,
        menu_search_service: MenuSearchService,
        recipe_search_service: RecipeSearchService,
    ) -> None:
        self._inventory_search_service = inventory_search_service
        self._inventory_modification_service = inventory_modification_service
        self._menu_search_service = menu_search_service
        self._recipe_search_service = recipe_search_service
        logger.debug("Initialized %s.", self.__class__.__name__)

    def _map_inventory(self) -> dict[tuple[str, str], InventoryItem]:
        mapped = {}
        for item in self._inventory_search_service.get_all():
            _, std_unit = standardize_unit(item.quantity, item.unit)
            mapped[(item.name, std_unit)] = item
        return mapped

    def apply_shopping_list(self, shopping_list: ShoppingList) -> None:
        inventory_map = self._map_inventory()
        for item in shopping_list.items:
            std_qty, std_unit = standardize_unit(item.quantity, item.unit)
            key = (item.name, std_unit)
            existing_item = inventory_map.get(key)
            if existing_item:
                existing_std_qty, _ = standardize_unit(
                    existing_item.quantity, existing_item.unit
                )
                new_qty = existing_std_qty + std_qty
                updated_item = replace(existing_item, quantity=new_qty, unit=std_unit)
                self._inventory_modification_service.modify(updated_item)
            else:
                new_item = InventoryItem(
                    name=item.name, quantity=item.quantity, unit=item.unit
                )
                self._inventory_modification_service.create(new_item)
        logger.info(
            "Updated inventory after applying shopping list with ID '%s'.",
            shopping_list.id,
        )

    def consume_meals_for_period(self, start_date: date, end_date: date) -> None:
        validate_date_range(start_date, end_date)
        menus = self._menu_search_service.filter_by_date_range(start_date, end_date)
        consumed_totals = calculate_menu_ingredients(menus, self._recipe_search_service)
        if not consumed_totals:
            logger.warning(
                "Found no meals for period '%s' to '%s'.", start_date, end_date
            )
            return
        inventory_map = self._map_inventory()
        deducted_count = 0
        for (name, std_unit), consumed_qty in consumed_totals.items():
            existing_item = inventory_map.get((name, std_unit))
            if existing_item and existing_item.quantity > 0:
                existing_std_qty, _ = standardize_unit(
                    existing_item.quantity, existing_item.unit
                )
                new_qty = max(0.0, existing_std_qty - consumed_qty)
                updated_item = replace(existing_item, quantity=new_qty, unit=std_unit)
                self._inventory_modification_service.modify(updated_item)
                deducted_count += 1
        if deducted_count > 0:
            logger.info(
                "Deducted inventory items for meals consumed between '%s' and '%s'.",
                start_date,
                end_date,
            )
        else:
            logger.warning(
                "Found no matching inventory items for meals consumed between '%s' and '%s'.",
                start_date,
                end_date,
            )
