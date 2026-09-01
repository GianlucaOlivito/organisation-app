import logging
from collections import defaultdict
from datetime import date

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
        logger.debug("ShoppingListService initialized.")

    def generate_shopping_list(self, start_date: date, end_date: date) -> ShoppingList:
        if start_date > end_date:
            logger.warning(
                f"Shopping list generation failed: start_date ({start_date}) is after end_date ({end_date})."
            )
            raise ValueError("INVALID ARGUMENT: Start date cannot be after end date.")

        # 1. Fetch menus in date range
        menus = self._menu_search_service.filter_by_date_range(start_date, end_date)

        # 2. Aggregate needed ingredients from recipes in scheduled menus
        # Key: (ingredient_name, unit) -> Value: total_quantity
        needed_totals: dict[tuple[str, str], float] = defaultdict(float)

        for menu in menus:
            for course in menu.courses:
                recipe = self._recipe_search_service.get_by_id(course.recipe_id)
                if recipe is None:
                    logger.warning(
                        f"Recipe with ID '{course.recipe_id}' referenced in menu '{menu.id}' not found."
                    )
                    continue
                for ingredient in recipe.ingredients:
                    key = (ingredient.name, ingredient.unit)
                    needed_totals[key] += ingredient.quantity * course.portions

        # 3. Aggregate available inventory stock
        inventory_items = self._inventory_search_service.get_all()
        available_totals: dict[tuple[str, str], float] = defaultdict(float)

        for item in inventory_items:
            key = (item.name, item.unit)
            available_totals[key] += item.quantity

        # 4. Subtract inventory from needed ingredients
        shopping_items: list[ShoppingListItem] = []

        for (name, unit), required_qty in needed_totals.items():
            available_qty = available_totals.get((name, unit), 0.0)
            needed_qty = required_qty - available_qty

            if needed_qty > 0:
                shopping_items.append(
                    ShoppingListItem(name=name, quantity=needed_qty, unit=unit)
                )

        logger.info(
            f"Generated shopping list with {len(shopping_items)} item(s) for period {start_date} to {end_date}."
        )
        return ShoppingList(items=shopping_items)
