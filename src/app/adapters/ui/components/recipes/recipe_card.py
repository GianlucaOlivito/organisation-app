from collections.abc import Callable
from uuid import UUID

import flet as ft

from app.adapters.ui.components.common.base_card import BaseCard
from app.adapters.ui.components.common.controls import create_divider, create_text
from app.adapters.ui.theme import theme
from app.domain.recipes.recipe import Recipe
from app.domain.recipes.recipe_ingredient import RecipeIngredient


class RecipeCard(BaseCard[Recipe]):
    """Represents a component to display a single Recipe entity."""

    def __init__(
        self,
        recipe: Recipe,
        on_edit: Callable[[Recipe], None] | None = None,
        on_delete: Callable[[UUID], None] | None = None,
    ) -> None:
        self.recipe = recipe
        super().__init__(entity=recipe, on_edit=on_edit, on_delete=on_delete)

    @staticmethod
    def _format_ingredient(ing: RecipeIngredient) -> str:
        qty = int(ing.quantity) if ing.quantity.is_integer() else ing.quantity
        unit_str = f" {ing.unit}" if ing.unit else ""
        return f"• {qty}{unit_str} {ing.name}"

    def _build_ingredients_section(self) -> ft.Control:
        ing_controls = [
            create_text(self._format_ingredient(ing), size=theme.font_size_small)
            for ing in self.recipe.ingredients
        ]
        return ft.Column(
            controls=[create_text("Zutaten"), *ing_controls],
            spacing=theme.spacing_small,
        )

    def _build_instructions_section(self) -> ft.Control:
        return ft.Column(
            controls=[
                create_text("Zubereitung"),
                create_text(
                    self.recipe.instructions.strip(), size=theme.font_size_small
                ),
            ],
            spacing=theme.spacing_small,
        )

    def _build_card_content(self) -> list[ft.Control]:
        return [
            self._build_header(
                title=self.recipe.name.strip(), entity_id=self.recipe.id
            ),
            create_divider(),
            self._build_ingredients_section(),
            create_divider(),
            self._build_instructions_section(),
        ]
