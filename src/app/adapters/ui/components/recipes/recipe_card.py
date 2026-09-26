from collections.abc import Callable
from uuid import UUID

import flet as ft

from app.adapters.ui.components.common.controls import (
    create_container,
    create_delete_button,
    create_divider,
    create_edit_button,
    create_header,
    create_muted_text,
    create_text,
)
from app.adapters.ui.theme import theme
from app.domain.recipes.recipe import Recipe
from app.domain.recipes.recipe_ingredient import RecipeIngredient


class RecipeCard(ft.Card):
    """Represents a component to display a single Recipe entity."""

    def __init__(
        self,
        recipe: Recipe,
        on_edit: Callable[[Recipe], None] | None = None,
        on_delete: Callable[[UUID], None] | None = None,
    ) -> None:
        self.recipe = recipe
        self.on_edit = on_edit
        self.on_delete = on_delete
        super().__init__(
            content=create_container(
                content=ft.Column(
                    controls=[
                        self._build_header(),
                        create_divider(),
                        self._build_ingredients_section(),
                        create_divider(),
                        self._build_instructions_section(),
                    ],
                    spacing=theme.spacing_medium,
                    scroll=ft.ScrollMode.AUTO,
                    expand=True,
                ),
            )
        )

    @staticmethod
    def _format_ingredient(ing: RecipeIngredient) -> str:
        qty = int(ing.quantity) if ing.quantity.is_integer() else ing.quantity
        unit_str = f" {ing.unit}" if ing.unit else ""
        return f"• {qty}{unit_str} {ing.name}"

    def _build_header(self) -> ft.Control:
        action_controls = []
        if self.on_edit:
            action_controls.append(
                create_edit_button(on_click=lambda _: self.on_edit(self.recipe))
            )
        if self.on_delete:
            action_controls.append(
                create_delete_button(on_click=lambda _: self.on_delete(self.recipe.id))
            )
        return ft.Row(
            controls=[
                create_header(self.recipe.name.strip(), expand=True),
                ft.Row(
                    controls=[
                        create_muted_text(f"ID: {str(self.recipe.id)[:8]}"),
                        *action_controls,
                    ],
                    spacing=theme.spacing_small,
                    vertical_alignment=ft.CrossAxisAlignment.CENTER,
                ),
            ],
            alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
        )

    def _build_ingredients_section(self) -> ft.Control:
        ing_controls = [
            create_text(self._format_ingredient(ing), size=theme.font_size_small)
            for ing in self.recipe.ingredients
        ]
        return ft.Column(
            controls=[
                create_text("Zutaten", weight=theme.font_weight_semibold),
                *ing_controls,
            ],
            spacing=theme.spacing_small,
        )

    def _build_instructions_section(self) -> ft.Control:
        return ft.Column(
            controls=[
                create_text("Zubereitung", weight=theme.font_weight_semibold),
                create_text(self.recipe.instructions.strip()),
            ],
            spacing=theme.spacing_small,
        )
