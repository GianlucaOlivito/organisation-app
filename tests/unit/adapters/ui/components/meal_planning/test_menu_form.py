from datetime import date
from uuid import uuid4

import flet as ft

from app.domain.meal_planning.menu import Menu
from tests.fixtures.ui import UpdateSpy


def test_initialization_creation_mode(menu_form):
    assert menu_form._menu_id is not None
    assert menu_form._description_field.value == ""
    assert menu_form._date_field.value == ""
    assert len(menu_form._courses_column.controls) == 1


def test_initialization_edit_mode(sample_menus, menu_form):
    menu_to_edit = sample_menus[0]
    menu_form.__init__(menu=menu_to_edit)
    menu_form.update = UpdateSpy()

    assert menu_form._menu_id == menu_to_edit.id
    assert menu_form._description_field.value == menu_to_edit.description
    assert menu_form._date_field.value == str(menu_to_edit.scheduled_date)
    assert len(menu_form._courses_column.controls) == len(menu_to_edit.courses)

    first_row = menu_form._courses_column.controls[0]

    assert first_row.controls[0].value == str(menu_to_edit.courses[0].recipe_id)
    assert first_row.controls[1].value == str(menu_to_edit.courses[0].portions)


def test_add_course_row(menu_form):
    recipe_id = str(uuid4())
    initial_count = len(menu_form._courses_column.controls)
    menu_form._add_course_row(recipe_id, "4")

    assert len(menu_form._courses_column.controls) == initial_count + 1

    new_row = menu_form._courses_column.controls[-1]

    assert isinstance(new_row, ft.Row)
    assert new_row.controls[0].value == recipe_id
    assert new_row.controls[1].value == "4"


def test_delete_course_row(menu_form):
    recipe_id = str(uuid4())
    menu_form._add_course_row(recipe_id, "2")

    assert len(menu_form._courses_column.controls) == 2

    delete_button = menu_form._courses_column.controls[1].controls[2]
    delete_button.on_click(UpdateSpy())

    assert len(menu_form._courses_column.controls) == 1


def test_extract_entity_constructs_valid_domain_model(menu_form):
    recipe_id = uuid4()
    menu_form._description_field.value = " Sunday Dinner "
    menu_form._date_field.value = " 2026-10-01 "
    row = menu_form._courses_column.controls[0]
    row.controls[0].value = f" {recipe_id} "
    row.controls[1].value = " 4 "
    menu = menu_form._extract_entity()

    assert isinstance(menu, Menu)
    assert menu.id == menu_form._menu_id
    assert menu.description == "Sunday Dinner"
    assert menu.scheduled_date == date(2026, 10, 1)
    assert len(menu.courses) == 1
    assert menu.courses[0].recipe_id == recipe_id
    assert menu.courses[0].portions == 4


def test_extract_entity_filters_out_completely_empty_rows(menu_form):
    recipe_id = uuid4()
    menu_form._description_field.value = "Quick Lunch"
    menu_form._date_field.value = "2026-10-02"
    row1 = menu_form._courses_column.controls[0]
    row1.controls[0].value = str(recipe_id)
    row1.controls[1].value = "2"
    menu_form._add_course_row("", "")
    menu = menu_form._extract_entity()

    assert len(menu.courses) == 1
    assert menu.courses[0].recipe_id == recipe_id
    assert menu.courses[0].portions == 2


def test_handle_save_success(menu_form):
    recipe_id = uuid4()
    on_save = UpdateSpy()
    menu_form._on_save = on_save
    menu_form._description_field.value = "Birthday Feast"
    menu_form._date_field.value = "2026-10-05"
    row = menu_form._courses_column.controls[0]
    row.controls[0].value = str(recipe_id)
    row.controls[1].value = "6"
    menu_form._handle_save(UpdateSpy())

    assert menu_form._error_text.visible is False
    on_save.assert_called_once()

    saved_menu = on_save.call_args[0]

    assert saved_menu.description == "Birthday Feast"


def test_handle_save_displays_error_on_validation_failure(menu_form):
    on_save = UpdateSpy()
    menu_form._on_save = on_save
    menu_form._extract_entity = lambda: (_ for _ in ()).throw(
        ValueError("Description cannot be empty")
    )
    menu_form._handle_save(UpdateSpy())

    assert menu_form._error_text.visible is True
    assert menu_form._error_text.value == "Description cannot be empty"
    on_save.assert_not_called()
    menu_form.update.assert_called_once()


def test_close_button_triggers_on_close_callback(menu_form):
    on_close = UpdateSpy()
    menu_form._on_close = on_close
    header_row = menu_form.controls[0]
    header_action_row = header_row.controls[1]
    close_button = header_action_row.controls[-1]
    close_button.on_click(UpdateSpy())

    on_close.assert_called_once()
