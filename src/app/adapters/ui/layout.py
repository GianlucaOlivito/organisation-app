import flet as ft

from .components.sidebar import NavigationItemConfig, Sidebar
from .views.inventory_view import InventoryView
from .views.menus_view import MenusView
from .views.recipes_view import RecipesView
from .views.shopping_list_view import ShoppingListView


class AppLayout(ft.Row):
    """Application layout shell coordinating navigation and view containers."""

    def __init__(self) -> None:
        self._views = [
            RecipesView(),
            MenusView(),
            InventoryView(),
            ShoppingListView(),
        ]
        navigation_item_configs = [
            NavigationItemConfig(icon=ft.Icons.RESTAURANT_MENU, label="Recipes"),
            NavigationItemConfig(icon=ft.Icons.CALENDAR_MONTH, label="Menus"),
            NavigationItemConfig(icon=ft.Icons.INVENTORY_2, label="Inventory"),
            NavigationItemConfig(icon=ft.Icons.SHOPPING_CART, label="Shopping"),
        ]
        self._sidebar = Sidebar(
            items=navigation_item_configs,
            selected_index=0,
            on_change=self._switch_tab,
        )
        self._content_area = ft.Container(
            content=self._views[0],
            expand=True,
            padding=20,
        )
        super().__init__(
            expand=True,
            spacing=0,
            controls=[
                self._sidebar,
                ft.VerticalDivider(width=1),
                self._content_area,
            ],
        )

    def _switch_tab(self, index: int) -> None:
        self._content_area.content = self._views[index]
        self._content_area.update()
