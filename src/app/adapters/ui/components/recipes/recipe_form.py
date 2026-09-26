from collections.abc import Callable
from uuid import UUID, uuid4

import flet as ft

from app.adapters.ui.components.common.controls import (
    create_add_button,
    create_close_button,
    create_container,
    create_delete_button,
    create_divider,
    create_header,
    create_save_button,
    create_text,
    create_text_field,
    create_title,
)
from app.adapters.ui.theme import theme
from app.domain.recipes.recipe import Recipe
from app.domain.recipes.recipe_ingredient import RecipeIngredient


class RecipeForm(ft.Column):
    """Represents a form component for creating and editing recipes."""

    def __init__(
        self,
        recipe: Recipe | None = None,
        on_save: Callable[[Recipe], None] | None = None,
        on_close: Callable[[], None] | None = None,
    ) -> None:
        super().__init__(
            spacing=theme.spacing_medium,
            scroll=ft.ScrollMode.AUTO,
            expand=True,
        )
        self._recipe_id: UUID = recipe.id if recipe else uuid4()
        self._on_save = on_save
        header_row = ft.Row(
            controls=[
                create_title("Rezept modifizieren" if recipe else "Rezept erstellen"),
                ft.Row(
                    controls=[
                        create_save_button(on_click=self._handle_save),
                        create_close_button(
                            on_click=lambda _: on_close() if on_close else None
                        ),
                    ]
                ),
            ],
            alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
        )
        self._name_field = create_text_field(
            value=recipe.name if recipe else "",
            hint_text="Rezeptname",
        )
        self._error_text = create_text(
            value="",
            color=theme.color_danger,
            size=theme.font_size_small,
            visible=False,
        )
        self._instructions_field = create_text_field(
            value=recipe.instructions if recipe else "",
            hint_text="Zubereitung",
            multiline=True,
            min_lines=theme.input_field_min_lines,
            max_lines=theme.input_field_max_lines,
        )
        self._ingredients_column = ft.Column(
            spacing=theme.spacing_small,
            scroll=ft.ScrollMode.AUTO,
        )
        ingredients_header = ft.Row(
            controls=[
                create_header("Zutaten"),
                create_add_button(on_click=lambda _: self._add_ingredient_row()),
            ],
            alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
        )
        ingredients_container = create_container(
            content=self._ingredients_column,
            height=theme.container_height_medium,
            padding=theme.spacing_none,
        )
        if recipe and recipe.ingredients:
            for ing in recipe.ingredients:
                self._add_ingredient_row(
                    name=ing.name,
                    quantity=str(ing.quantity),
                    unit=ing.unit,
                )
        else:
            self._add_ingredient_row()
        self.controls = [
            header_row,
            create_divider(),
            self._error_text,
            self._name_field,
            create_divider(),
            ingredients_header,
            ingredients_container,
            create_divider(),
            self._instructions_field,
        ]

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

    def get_recipe(self) -> Recipe:
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

    def _handle_save(self, e: ft.ControlEvent) -> None:
        try:
            recipe = self.get_recipe()
            self._error_text.visible = False
            if self._on_save:
                self._on_save(recipe)
        except (TypeError, ValueError) as err:
            self._error_text.value = str(err)
            self._error_text.visible = True
            self.update()
