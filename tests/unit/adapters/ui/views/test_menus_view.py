from unittest.mock import MagicMock

import flet as ft

from app.adapters.ui.components.meal_planning.menu_card import MenuCard
from app.adapters.ui.components.meal_planning.menu_form import MenuForm


def test_initialization_renders_sample_menus(menus_view, sample_menus):
    assert len(menus_view._grid.controls) == len(sample_menus)
    assert isinstance(menus_view._grid.controls[0], MenuCard)
    assert menus_view._grid.controls[0].menu == sample_menus[0]


def test_search_by_id(menus_view, sample_menus):
    target_menu = sample_menus[0]
    menus_view._search_input.value = str(target_menu.id)
    menus_view._search()

    assert len(menus_view._grid.controls) == 1
    assert menus_view._grid.controls[0].menu.id == target_menu.id


def test_search_empty_state_when_no_match(menus_view):
    menus_view._search_input.value = "00000000-0000-0000-0000-000000000000"
    menus_view._search()

    assert menus_view._content_container.controls == [menus_view._empty_state]


def test_filter_by_date_range(menus_view, sample_menus):
    target_menu = sample_menus[0]
    formatted_date = target_menu.scheduled_date.strftime("%d.%m.%Y")
    menus_view._start_date_input.value = formatted_date
    menus_view._end_date_input.value = formatted_date
    menus_view._filter()

    assert len(menus_view._grid.controls) == 1
    assert menus_view._grid.controls[0].menu.id == target_menu.id


def test_search_and_filter_reset_opposite_channel(menus_view, sample_menus):
    menus_view._search_input.value = str(sample_menus[0].id)
    menus_view._start_date_input.value = "01.01.2000"
    menus_view._end_date_input.value = "02.01.2000"
    menus_view._filter()

    assert menus_view._content_container.controls == [menus_view._empty_state]


def test_toolbar_structure(menus_view):
    toolbar = menus_view._toolbar

    assert isinstance(toolbar, ft.Row)
    assert len(toolbar.controls) == 6
    assert toolbar.controls[0] == menus_view._add_button
    assert toolbar.controls[1] == menus_view._search_button
    assert toolbar.controls[2] == menus_view._search_input
    assert toolbar.controls[3] == menus_view._filter_button
    assert toolbar.controls[4] == menus_view._start_date_input
    assert toolbar.controls[5] == menus_view._end_date_input


def test_open_form_for_creation(menus_view):
    menus_view._open_form()

    assert menus_view._toolbar.visible is False
    assert len(menus_view._content_container.controls) == 1

    form = menus_view._content_container.controls[0]

    assert isinstance(form, MenuForm)
    assert form._menu_id is not None


def test_open_form_for_editing(menus_view, sample_menus):
    menu_to_edit = sample_menus[0]
    menus_view._open_form(menu_to_edit)

    assert menus_view._toolbar.visible is False
    assert len(menus_view._content_container.controls) == 1

    form = menus_view._content_container.controls[0]

    assert isinstance(form, MenuForm)
    assert form._menu_id == menu_to_edit.id


def test_close_form_restores_toolbar(menus_view):
    menus_view._open_form()
    menus_view._close_form()

    assert menus_view._toolbar.visible is True


def test_save_form_creates_and_modifies_menu(
    menus_view, meal_planning_modification_service, sample_menus
):
    meal_planning_modification_service.create = MagicMock()
    meal_planning_modification_service.modify = MagicMock()
    menus_view._open_form()
    form = menus_view._content_container.controls[0]
    form._on_save(sample_menus[0])
    meal_planning_modification_service.create.assert_called_once_with(sample_menus[0])

    menus_view._open_form(sample_menus[1])
    form = menus_view._content_container.controls[0]
    form._on_save(sample_menus[1])

    meal_planning_modification_service.modify.assert_called_once_with(sample_menus[1])


def test_delete_menu(menus_view, sample_menus):
    menu_to_delete = sample_menus[0]
    initial_count = len(menus_view._grid.controls)
    menus_view._delete_menu(menu_to_delete.id)

    assert len(menus_view._grid.controls) == initial_count - 1
    assert all(card.menu.id != menu_to_delete.id for card in menus_view._grid.controls)


def test_refresh_triggers_search(menus_view, sample_menus):
    target_menu = sample_menus[0]
    menus_view._search_input.value = str(target_menu.id)
    menus_view.refresh()

    assert len(menus_view._grid.controls) == 1
    assert menus_view._grid.controls[0].menu.id == target_menu.id
