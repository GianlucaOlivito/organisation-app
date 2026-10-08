import flet as ft

from app.adapters.ui.components.common.controls import (
    create_container,
    create_vertical_divider,
)
from app.adapters.ui.theme import theme
from app.infrastructure.container import Container

from .components.common.sidebar import Sidebar
from .views.inventory_view import InventoryView
from .views.logs_view import LogsView
from .views.menus_view import MenusView
from .views.recipes_view import RecipesView
from .views.shopping_list_view import ShoppingListView


class AppLayout(ft.Row):
    """Application layout shell coordinating navigation and view containers."""

    def __init__(self, container: Container) -> None:
        self._views = [
            RecipesView(
                container.recipe_modification_service,
                container.recipe_search_service,
            ),
            MenusView(
                container.menu_modification_service,
                container.menu_search_service,
                container.recipe_search_service,
            ),
            InventoryView(
                container.inventory_modification_service,
                container.inventory_search_service,
            ),
            ShoppingListView(
                container.settings,
                container.shopping_list_service,
                container.inventory_reconciliation_service,
            ),
            LogsView(container.log_buffer),
        ]
        nav_items = [
            (ft.Icons.RESTAURANT_MENU, "Rezepte"),
            (ft.Icons.CALENDAR_MONTH, "Menüplanung"),
            (ft.Icons.INVENTORY_2, "Vorrat"),
            (ft.Icons.SHOPPING_CART, "Einkauf"),
            (ft.Icons.TERMINAL, "Logdaten"),
        ]
        self._sidebar = Sidebar(items=nav_items, on_change=self._switch_tab)
        self._content_area = create_container(content=self._views[0], expand=True)
        super().__init__(
            expand=True,
            spacing=theme.spacing_none,
            controls=[self._sidebar, create_vertical_divider(), self._content_area],
        )

    def _switch_tab(self, index: int) -> None:
        view = self._views[index]
        if hasattr(view, "refresh"):
            view.refresh()
        self._content_area.content = view
        self._content_area.update()
