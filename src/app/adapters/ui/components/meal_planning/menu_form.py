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
from app.domain.meal_planning.course import Course
from app.domain.meal_planning.menu import Menu


class MenuForm(ft.Column):
    """Represents a form component for creating and editing menus."""

    def __init__(
        self,
        menu: Menu | None = None,
        on_save: Callable[[Menu], None] | None = None,
        on_close: Callable[[], None] | None = None,
    ) -> None:
        super().__init__(
            spacing=theme.spacing_medium,
            scroll=ft.ScrollMode.AUTO,
            expand=True,
        )
        self._menu_id: UUID = menu.id if menu else uuid4()
        self._on_save = on_save
        header_row = ft.Row(
            controls=[
                create_title("Menü modifizieren" if menu else "Menü erstellen"),
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
        self._description_field = create_text_field(
            value=menu.description if menu else "",
            hint_text="Menübeschreibung",
        )
        self._error_text = create_text(
            value="",
            color=theme.color_danger,
            size=theme.font_size_small,
            visible=False,
        )
        self._date_field = create_text_field(
            value=str(menu.scheduled_date) if menu else "",
            hint_text="Datum",
        )
        self._courses_column = ft.Column(
            spacing=theme.spacing_small,
            scroll=ft.ScrollMode.AUTO,
        )
        courses_header = ft.Row(
            controls=[
                create_header("Gänge"),
                create_add_button(on_click=lambda _: self._add_course_row()),
            ],
            alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
        )
        courses_container = create_container(
            content=self._courses_column,
            height=theme.container_height_medium,
            padding=theme.spacing_none,
        )
        if menu and menu.courses:
            for course in menu.courses:
                self._add_course_row(
                    recipe_id=str(course.recipe_id),
                    portions=str(course.portions),
                )
        else:
            self._add_course_row()
        self.controls = [
            header_row,
            create_divider(),
            self._error_text,
            self._description_field,
            create_divider(),
            self._date_field,
            create_divider(),
            courses_header,
            courses_container,
        ]

    def _add_course_row(self, recipe_id: str = "", portions: str = "") -> None:
        recipe_id_field = create_text_field(hint_text="Rezept-ID", value=recipe_id)
        portions_field = create_text_field(hint_text="Portionen", value=portions)
        row = ft.Row(spacing=theme.spacing_small)

        def _delete_row(_: ft.ControlEvent) -> None:
            self._courses_column.controls.remove(row)

        del_btn = create_delete_button(on_click=_delete_row)
        row.controls = [recipe_id_field, portions_field, del_btn]
        self._courses_column.controls.append(row)

    def get_menu(self) -> Menu:
        courses: list[Course] = []
        for row in self._courses_column.controls:
            if not isinstance(row, ft.Row):
                continue
            recipe_id = (row.controls[0].value or "").strip()
            portions = (row.controls[1].value or "").strip()
            if not recipe_id and not portions:
                continue
            courses.append(Course(recipe_id=recipe_id, portions=portions))
        return Menu(
            id=self._menu_id,
            description=(self._description_field.value or "").strip(),
            scheduled_date=(self._date_field.value or "").strip(),
            courses=courses,
        )

    def _handle_save(self, e: ft.ControlEvent) -> None:
        try:
            menu = self.get_menu()
            self._error_text.visible = False
            if self._on_save:
                self._on_save(menu)
        except (TypeError, ValueError) as err:
            self._error_text.value = str(err)
            self._error_text.visible = True
            self.update()
