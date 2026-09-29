import flet as ft

from app.adapters.ui.components.meal_planning.menu_card import MenuCard


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
    toolbar = menus_view.controls[2]

    assert isinstance(toolbar, ft.Row)
    assert len(toolbar.controls) == 5
    assert toolbar.controls[0] == menus_view._search_button
    assert toolbar.controls[1] == menus_view._search_input
    assert toolbar.controls[2] == menus_view._filter_button
    assert toolbar.controls[3] == menus_view._start_date_input
    assert toolbar.controls[4] == menus_view._end_date_input
