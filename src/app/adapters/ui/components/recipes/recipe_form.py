from collections.abc import Callable
from uuid import UUID, uuid4

import flet as ft

from app.adapters.ui.components.common.base_form import BaseForm
from app.adapters.ui.components.common.controls import (
    create_add_button,
    create_container,
    create_delete_button,
    create_divider,
    create_text,
    create_text_field,
)
from app.adapters.ui.theme import theme
from app.domain.recipes.recipe import Recipe
from app.domain.recipes.recipe_ingredient import RecipeIngredient


class RecipeForm(BaseForm[Recipe]):
    """Represents a form component for creating and editing recipes."""

    def __init__(
        self,
        recipe: Recipe | None = None,
        on_save: Callable[[Recipe], None] | None = None,
        on_close: Callable[[], None] | None = None,
    ) -> None:
        self._recipe = recipe
        self._recipe_id: UUID = recipe.id if recipe else uuid4()
        self._name_field = create_text_field(
            value=recipe.name if recipe else "",
            hint_text="Rezeptname",
        )
        self._instructions_field = create_text_field(
            value=recipe.instructions if recipe else "",
            hint_text="Zubereitung",
            multiline=True,
            min_lines=theme.input_field_min_lines,
        )
        self._ingredients_column = ft.Column(spacing=theme.spacing_small)
        super().__init__(
            title="Rezept modifizieren" if recipe else "Rezept erstellen",
            on_save=on_save,
            on_close=on_close,
        )

    def _add_ingredient_row(
        self, name: str = "", quantity: str = "", unit: str = ""
    ) -> None:
        name_field = create_text_field(hint_text="Zutatenname", value=name)
        qty_field = create_text_field(hint_text="Menge", value=quantity)
        unit_field = create_text_field(hint_text="Einheit", value=unit)
        row = ft.Row(spacing=theme.spacing_small)

        def _delete_row(_: ft.ControlEvent) -> None:
            self._ingredients_column.controls.remove(row)

        del_btn = create_delete_button(on_click=_delete_row)
        row.controls = [name_field, qty_field, unit_field, del_btn]
        self._ingredients_column.controls.append(row)

    def _extract_entity(self) -> Recipe:
        ingredients: list[RecipeIngredient] = []
        for row in self._ingredients_column.controls:
            if not isinstance(row, ft.Row):
                continue
            ing_name = (row.controls[0].value or "").strip()
            qty = (row.controls[1].value or "").strip()
            unit = (row.controls[2].value or "").strip()
            if not ing_name and not qty and not unit:
                continue
            ingredients.append(RecipeIngredient(name=ing_name, quantity=qty, unit=unit))
        return Recipe(
            id=self._recipe_id,
            name=(self._name_field.value or "").strip(),
            ingredients=ingredients,
            instructions=(self._instructions_field.value or "").strip(),
        )

    def _build_form_controls(self) -> list[ft.Control]:
        ingredients_header = ft.Row(
            controls=[
                create_text("Zutaten"),
                create_add_button(on_click=lambda _: self._add_ingredient_row()),
            ],
            alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
        )
        ingredients_container = create_container(
            content=self._ingredients_column,
            padding=theme.spacing_none,
        )
        if self._recipe and self._recipe.ingredients:
            for ing in self._recipe.ingredients:
                self._add_ingredient_row(
                    name=ing.name,
                    quantity=str(ing.quantity),
                    unit=ing.unit,
                )
        else:
            self._add_ingredient_row()
        return [
            self._name_field,
            create_divider(),
            ingredients_header,
            ingredients_container,
            create_divider(),
            self._instructions_field,
        ]
