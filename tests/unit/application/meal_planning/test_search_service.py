from datetime import date
from uuid import uuid4

import pytest

from app.application.meal_planning.search_service import MenuSearchService
from app.domain.meal_planning.menu import Menu


@pytest.fixture
def search_service(fake_menu_repo) -> MenuSearchService:
    return MenuSearchService(menu_repository=fake_menu_repo)


@pytest.fixture
def sample_menus(fake_menu_repo) -> list[Menu]:
    menu1 = Menu(
        id=uuid4(),
        scheduled_date=date(2026, 9, 1),
        description="Lunch",
        courses=[],
    )
    menu2 = Menu(
        id=uuid4(),
        scheduled_date=date(2026, 9, 10),
        description="Dinner",
        courses=[],
    )
    fake_menu_repo.save(menu1)
    fake_menu_repo.save(menu2)
    return [menu1, menu2]


def test_get_all_returns_empty_list_when_no_menus(search_service):
    assert search_service.get_all() == []


def test_get_all_returns_all_menus(search_service, sample_menus):
    results = search_service.get_all()
    assert len(results) == 2
    assert results == sample_menus


def test_get_by_id_returns_menu_when_found(search_service, sample_menus):
    expected_menu = sample_menus[0]
    found_menu = search_service.get_by_id(expected_menu.id)
    assert found_menu == expected_menu


def test_get_by_id_returns_none_when_not_found(search_service):
    assert search_service.get_by_id(uuid4()) is None


def test_filter_by_date_range_returns_matching_menus(search_service, sample_menus):
    start_date = date(2026, 8, 30)
    end_date = date(2026, 9, 5)
    results = search_service.filter_by_date_range(start_date, end_date)

    assert len(results) == 1
    assert results[0] == sample_menus[0]


def test_filter_by_date_range_returns_empty_list_when_no_match(
    search_service, sample_menus
):
    start_date = date(2026, 9, 15)
    end_date = date(2026, 9, 20)
    results = search_service.filter_by_date_range(start_date, end_date)

    assert results == []
