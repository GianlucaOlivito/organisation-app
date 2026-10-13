import json
import logging
from datetime import date
from uuid import uuid4

from app.domain.meal_planning.menu import Menu


def test_get_all_returns_empty_list_when_file_does_not_exist(json_menu_repo):
    assert json_menu_repo.get_all() == []


def test_save_and_get_all(json_menu_repo, sample_menus):
    sample_menu = sample_menus[0]
    json_menu_repo.save(sample_menu)
    menus = json_menu_repo.get_all()

    assert len(menus) == 1
    assert menus[0].id == sample_menu.id
    assert menus[0].description == sample_menu.description
    assert menus[0].scheduled_date == sample_menu.scheduled_date
    assert len(menus[0].courses) == len(sample_menu.courses)


def test_get_all_skips_invalid_menu_entry(json_menu_repo, tmp_path, caplog):
    file_path = tmp_path / "menus.json"
    file_path.write_text(
        json.dumps(
            [
                {"id": "invalid-uuid", "description": "Bad Menu"},
                {
                    "id": "11111111-1111-1111-1111-111111111111",
                    "description": "Good Menu",
                    "scheduled_date": "2026-10-01",
                    "courses": [
                        {
                            "recipe_id": "22222222-2222-2222-2222-222222222222",
                            "portions": 1,
                        }
                    ],
                },
            ]
        ),
        encoding="utf-8",
    )
    with caplog.at_level(logging.ERROR):
        menus = json_menu_repo.get_all()

    assert len(menus) == 1
    assert menus[0].description == "Good Menu"
    assert "Failed to deserialize entity" in caplog.text


def test_get_by_id_returns_menu_when_found(json_menu_repo, sample_menus):
    sample_menu = sample_menus[0]
    json_menu_repo.save(sample_menu)
    found = json_menu_repo.get_by_id(sample_menu.id)

    assert found is not None
    assert found.id == sample_menu.id


def test_get_by_id_returns_none_when_not_found(json_menu_repo):
    assert json_menu_repo.get_by_id(uuid4()) is None


def test_filter_by_date_range_matches_in_range(json_menu_repo, sample_menus):
    menu1, menu2 = sample_menus
    json_menu_repo.save(menu1)
    json_menu_repo.save(menu2)

    matches = json_menu_repo.filter_by_date_range(
        start_date=date(2026, 8, 30),
        end_date=date(2026, 9, 2),
    )

    assert len(matches) == 1
    assert matches[0].id == menu1.id


def test_filter_by_date_range_returns_empty_when_no_match(json_menu_repo, sample_menus):
    sample_menu = sample_menus[0]
    json_menu_repo.save(sample_menu)
    matches = json_menu_repo.filter_by_date_range(
        start_date=date(2026, 11, 1),
        end_date=date(2026, 11, 30),
    )

    assert matches == []


def test_save_updates_existing_menu(json_menu_repo, sample_menus):
    sample_menu = sample_menus[0]
    json_menu_repo.save(sample_menu)
    updated_menu = Menu(
        id=sample_menu.id,
        description="Updated Menu Description",
        scheduled_date=sample_menu.scheduled_date,
        courses=sample_menu.courses,
    )
    json_menu_repo.save(updated_menu)
    menus = json_menu_repo.get_all()

    assert len(menus) == 1
    assert menus[0].description == "Updated Menu Description"


def test_delete_removes_menu(json_menu_repo, sample_menus):
    menu1, menu2 = sample_menus
    json_menu_repo.save(menu1)
    json_menu_repo.save(menu2)
    json_menu_repo.delete(menu1.id)
    menus = json_menu_repo.get_all()

    assert len(menus) == 1
    assert menus[0].id == menu2.id
