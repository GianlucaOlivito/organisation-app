from datetime import date
from uuid import uuid4


def test_get_all_returns_empty_list_when_no_menus(meal_planning_search_service):
    assert meal_planning_search_service.get_all() == []


def test_get_all_returns_all_menus(meal_planning_search_service, sample_menus):
    results = meal_planning_search_service.get_all()
    assert len(results) == 2
    assert results == sample_menus


def test_get_by_id_returns_menu_when_found(meal_planning_search_service, sample_menus):
    expected_menu = sample_menus[0]
    found_menu = meal_planning_search_service.get_by_id(expected_menu.id)
    assert found_menu == expected_menu


def test_get_by_id_returns_none_when_not_found(meal_planning_search_service):
    assert meal_planning_search_service.get_by_id(uuid4()) is None


def test_filter_by_date_range_returns_matching_menus(
    meal_planning_search_service, sample_menus
):
    start_date = date(2026, 8, 30)
    end_date = date(2026, 9, 5)
    results = meal_planning_search_service.filter_by_date_range(start_date, end_date)

    assert len(results) == 1
    assert results[0] == sample_menus[0]


def test_filter_by_date_range_returns_empty_list_when_no_match(
    meal_planning_search_service,
):
    start_date = date(2026, 9, 15)
    end_date = date(2026, 9, 20)
    results = meal_planning_search_service.filter_by_date_range(start_date, end_date)

    assert results == []
