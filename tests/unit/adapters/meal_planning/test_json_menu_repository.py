import json
import logging
from datetime import date
from pathlib import Path
from uuid import UUID, uuid4

import pytest

from app.adapters.meal_planning.json_menu_repository import JsonMenuRepository
from app.domain.meal_planning.course import Course
from app.domain.meal_planning.menu import Menu


@pytest.fixture
def sample_menu() -> Menu:
    return Menu(
        id=UUID("11111111-1111-1111-1111-111111111111"),
        description="Italian Dinner",
        scheduled_date=date(2026, 10, 1),
        courses=[
            Course(
                recipe_id=UUID("12345678-1234-5678-1234-567812345678"),
                portions=4.0,
            ),
        ],
    )


@pytest.fixture
def sample_menu_2() -> Menu:
    return Menu(
        id=UUID("22222222-2222-2222-2222-222222222222"),
        description="Sunday Lunch",
        scheduled_date=date(2026, 10, 5),
        courses=[
            Course(
                recipe_id=UUID("87654321-4321-8765-4321-876543218765"),
                portions=2.0,
            ),
        ],
    )


@pytest.fixture
def json_repo(tmp_path: Path) -> JsonMenuRepository:
    file_path = tmp_path / "menus.json"
    return JsonMenuRepository(file_path=file_path)


def test_get_all_returns_empty_list_when_file_does_not_exist(json_repo):
    assert json_repo.get_all() == []


def test_save_and_get_all(json_repo, sample_menu):
    json_repo.save(sample_menu)
    menus = json_repo.get_all()

    assert len(menus) == 1
    assert menus[0].id == sample_menu.id
    assert menus[0].description == sample_menu.description
    assert menus[0].scheduled_date == sample_menu.scheduled_date
    assert len(menus[0].courses) == 1


def test_get_all_skips_invalid_menu_entry(json_repo, tmp_path, caplog):
    file_path = tmp_path / "menus.json"
    file_path.write_text(
        json.dumps(
            [
                {"id": "invalid-uuid", "description": "Bad Menu"},
                {
                    "id": "11111111-1111-1111-1111-111111111111",
                    "description": "Good Menu",
                    "scheduled_date": "2026-10-01",
                    "courses": [],
                },
            ]
        ),
        encoding="utf-8",
    )
    with caplog.at_level(logging.ERROR):
        menus = json_repo.get_all()

    assert len(menus) == 1
    assert menus[0].description == "Good Menu"
    assert "Skipping invalid entity" in caplog.text


def test_get_by_id_returns_menu_when_found(json_repo, sample_menu):
    json_repo.save(sample_menu)
    found = json_repo.get_by_id(sample_menu.id)

    assert found is not None
    assert found.id == sample_menu.id


def test_get_by_id_returns_none_when_not_found(json_repo):
    assert json_repo.get_by_id(uuid4()) is None


def test_filter_by_date_range_matches_in_range(json_repo, sample_menu, sample_menu_2):
    json_repo.save(sample_menu)
    json_repo.save(sample_menu_2)
    matches = json_repo.filter_by_date_range(
        start_date=date(2026, 9, 30),
        end_date=date(2026, 10, 2),
    )

    assert len(matches) == 1
    assert matches[0].id == sample_menu.id


def test_filter_by_date_range_returns_empty_when_no_match(json_repo, sample_menu):
    json_repo.save(sample_menu)
    matches = json_repo.filter_by_date_range(
        start_date=date(2026, 11, 1),
        end_date=date(2026, 11, 30),
    )

    assert matches == []


def test_save_updates_existing_menu(json_repo, sample_menu):
    json_repo.save(sample_menu)
    updated_menu = Menu(
        id=sample_menu.id,
        description="Updated Italian Dinner",
        scheduled_date=sample_menu.scheduled_date,
        courses=sample_menu.courses,
    )
    json_repo.save(updated_menu)
    menus = json_repo.get_all()

    assert len(menus) == 1
    assert menus[0].description == "Updated Italian Dinner"


def test_delete_removes_menu(json_repo, sample_menu, sample_menu_2):
    json_repo.save(sample_menu)
    json_repo.save(sample_menu_2)
    json_repo.delete(sample_menu.id)
    menus = json_repo.get_all()

    assert len(menus) == 1
    assert menus[0].id == sample_menu_2.id


def test_delete_non_existent_menu_logs_warning(json_repo, caplog):
    non_existent_id = uuid4()
    with caplog.at_level(logging.WARNING):
        json_repo.delete(non_existent_id)

    assert (
        f"Attempted to delete non-existent entity with ID '{non_existent_id}'"
        in caplog.text
    )
