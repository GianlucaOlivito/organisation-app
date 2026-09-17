import flet as ft

from .views.inventory_view import InventoryView
from .views.menus_view import MenusView
from .views.recipes_view import RecipesView
from .views.shopping_list_view import ShoppingListView


class AppLayout(ft.Row):
    """Application layout containing navigation and dynamic content (views)."""

    def __init__(self) -> None:
        super().__init__(expand=True, spacing=0)
        self._views = [
            RecipesView(),
            MenusView(),
            InventoryView(),
            ShoppingListView(),
        ]
        self._content_area = ft.Container(
            content=self._views[0],
            expand=True,
            padding=20,
        )
        self._rail = ft.NavigationRail(
            selected_index=0,
            label_type=ft.NavigationRailLabelType.ALL,
            min_width=100,
            min_extended_width=200,
            destinations=[
                ft.NavigationRailDestination(
                    icon=ft.Icons.RESTAURANT_MENU, label="Recipes"
                ),
                ft.NavigationRailDestination(
                    icon=ft.Icons.CALENDAR_MONTH, label="Menus"
                ),
                ft.NavigationRailDestination(
                    icon=ft.Icons.INVENTORY_2, label="Inventory"
                ),
                ft.NavigationRailDestination(
                    icon=ft.Icons.SHOPPING_CART, label="Shopping"
                ),
            ],
            on_change=self._switch_tab,
        )
        self.controls = [
            self._rail,
            ft.VerticalDivider(width=1),
            self._content_area,
        ]

    def _switch_tab(self, e: ft.ControlEvent) -> None:
        selected_index = e.control.selected_index
        self._content_area.content = self._views[selected_index]
        self._content_area.update()
