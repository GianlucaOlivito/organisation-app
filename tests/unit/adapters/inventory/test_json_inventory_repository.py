import json
import logging
from pathlib import Path
from uuid import UUID, uuid4

import pytest

from app.adapters.inventory.json_inventory_repository import JsonInventoryRepository
from app.domain.inventory.inventory_item import InventoryItem


@pytest.fixture
def sample_item() -> InventoryItem:
    return InventoryItem(
        id=UUID("33333333-3333-3333-3333-333333333333"),
        name="Olive Oil",
        quantity=1.0,
        unit="l",
    )


@pytest.fixture
def sample_item_2() -> InventoryItem:
    return InventoryItem(
        id=UUID("44444444-4444-4444-4444-444444444444"),
        name="Flour",
        quantity=2.5,
        unit="kg",
    )


@pytest.fixture
def json_repo(tmp_path: Path) -> JsonInventoryRepository:
    file_path = tmp_path / "inventory.json"
    return JsonInventoryRepository(file_path=file_path)


def test_get_all_returns_empty_list_when_file_does_not_exist(json_repo):
    assert json_repo.get_all() == []


def test_save_and_get_all(json_repo, sample_item):
    json_repo.save(sample_item)
    items = json_repo.get_all()

    assert len(items) == 1
    assert items[0].id == sample_item.id
    assert items[0].name == sample_item.name
    assert items[0].quantity == sample_item.quantity
    assert items[0].unit == sample_item.unit


def test_get_all_skips_invalid_inventory_item(json_repo, tmp_path, caplog):
    file_path = tmp_path / "inventory.json"
    file_path.write_text(
        json.dumps(
            [
                {"id": "invalid-uuid", "name": "Bad Item"},
                {
                    "id": "33333333-3333-3333-3333-333333333333",
                    "name": "Good Item",
                    "quantity": 5.0,
                    "unit": "pcs",
                },
            ]
        ),
        encoding="utf-8",
    )
    with caplog.at_level(logging.ERROR):
        items = json_repo.get_all()

    assert len(items) == 1
    assert items[0].name == "Good Item"
    assert "Skipping invalid entity" in caplog.text


def test_get_by_id_returns_item_when_found(json_repo, sample_item):
    json_repo.save(sample_item)
    found = json_repo.get_by_id(sample_item.id)

    assert found is not None
    assert found.id == sample_item.id


def test_get_by_id_returns_none_when_not_found(json_repo):
    assert json_repo.get_by_id(uuid4()) is None


def test_get_by_name_case_and_whitespace_insensitive(json_repo, sample_item):
    json_repo.save(sample_item)
    found = json_repo.get_by_name("  OLIVE oil  ")

    assert found is not None
    assert found.id == sample_item.id


def test_get_by_name_returns_none_when_not_found(json_repo):
    assert json_repo.get_by_name("Non Existent Item") is None


def test_save_updates_existing_item(json_repo, sample_item):
    json_repo.save(sample_item)
    updated_item = InventoryItem(
        id=sample_item.id,
        name="Extra Virgin Olive Oil",
        quantity=2.0,
        unit="l",
    )
    json_repo.save(updated_item)
    items = json_repo.get_all()

    assert len(items) == 1
    assert items[0].name == "Extra Virgin Olive Oil"
    assert items[0].quantity == 2.0


def test_delete_removes_item(json_repo, sample_item, sample_item_2):
    json_repo.save(sample_item)
    json_repo.save(sample_item_2)
    json_repo.delete(sample_item.id)
    items = json_repo.get_all()

    assert len(items) == 1
    assert items[0].id == sample_item_2.id


def test_delete_non_existent_item_logs_warning(json_repo, caplog):
    non_existent_id = uuid4()
    with caplog.at_level(logging.WARNING):
        json_repo.delete(non_existent_id)

    assert (
        f"Attempted to delete non-existent entity with ID '{non_existent_id}'"
        in caplog.text
    )
