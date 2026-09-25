import flet as ft

from app.adapters.ui.components.common.controls import (
    create_container,
    create_divider,
    create_header,
    create_muted_text,
    create_text,
)
from app.adapters.ui.theme import theme
from app.domain.recipes.recipe import Recipe
from app.domain.recipes.recipe_ingredient import RecipeIngredient


class RecipeCard(ft.Card):
    """Represents a component to display a single Recipe entity."""

    def __init__(self, recipe: Recipe) -> None:
        self.recipe = recipe
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
        text = self.recipe.name.strip() or "Kein Name hinterlegt"
        return ft.Row(
            controls=[
                create_muted_text(text, expand=True)
                if not self.recipe.name.strip()
                else create_header(text, expand=True),
                create_muted_text(f"ID: {str(self.recipe.id)[:8]}"),
            ],
            alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
        )

    def _build_ingredients_section(self) -> ft.Control:
        if self.recipe.ingredients:
            ing_controls = [
                create_text(self._format_ingredient(ing), size=theme.font_size_small)
                for ing in self.recipe.ingredients
            ]
        else:
            ing_controls = [create_muted_text("Keine Zutaten hinterlegt")]
        return ft.Column(
            controls=[
                create_text("Zutaten", weight=theme.font_weight_semibold),
                *ing_controls,
            ],
            spacing=theme.spacing_small,
        )

    def _build_instructions_section(self) -> ft.Control:
        text = self.recipe.instructions.strip() or "Keine Zubereitung hinterlegt"
        return ft.Column(
            controls=[
                create_text("Zubereitung", weight=theme.font_weight_semibold),
                create_muted_text(text)
                if not self.recipe.instructions.strip()
                else create_text(text),
            ],
            spacing=theme.spacing_small,
        )
