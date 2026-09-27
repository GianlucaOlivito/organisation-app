import json
import logging
from uuid import uuid4

from app.domain.inventory.inventory_item import InventoryItem


def test_get_all_returns_empty_list_when_file_does_not_exist(json_inventory_repo):
    assert json_inventory_repo.get_all() == []


def test_save_and_get_all(json_inventory_repo, sample_items):
    sample_item = sample_items[0]
    json_inventory_repo.save(sample_item)
    items = json_inventory_repo.get_all()

    assert len(items) == 1
    assert items[0].id == sample_item.id
    assert items[0].name == sample_item.name
    assert items[0].quantity == sample_item.quantity
    assert items[0].unit == sample_item.unit


def test_get_all_skips_invalid_inventory_item(json_inventory_repo, tmp_path, caplog):
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
        items = json_inventory_repo.get_all()

    assert len(items) == 1
    assert items[0].name == "Good Item"
    assert "Failed to deserialize entity" in caplog.text


def test_get_by_id_returns_item_when_found(json_inventory_repo, sample_items):
    sample_item = sample_items[0]
    json_inventory_repo.save(sample_item)
    found = json_inventory_repo.get_by_id(sample_item.id)

    assert found is not None
    assert found.id == sample_item.id


def test_get_by_id_returns_none_when_not_found(json_inventory_repo):
    assert json_inventory_repo.get_by_id(uuid4()) is None


def test_get_by_name_case_and_whitespace_insensitive(json_inventory_repo, sample_items):
    sample_item = sample_items[0]
    json_inventory_repo.save(sample_item)
    found = json_inventory_repo.get_by_name("  mILk  ")

    assert found is not None
    assert found.id == sample_item.id


def test_get_by_name_returns_none_when_not_found(json_inventory_repo):
    assert json_inventory_repo.get_by_name("Non Existent Item") is None


def test_save_updates_existing_item(json_inventory_repo, sample_items):
    sample_item = sample_items[0]
    json_inventory_repo.save(sample_item)
    updated_item = InventoryItem(
        id=sample_item.id,
        name="Lactose Free Milk",
        quantity=2.0,
        unit="l",
    )
    json_inventory_repo.save(updated_item)
    items = json_inventory_repo.get_all()

    assert len(items) == 1
    assert items[0].name == "Lactose Free Milk"
    assert items[0].quantity == 2.0


def test_delete_removes_item(json_inventory_repo, sample_items):
    item1, item2 = sample_items
    json_inventory_repo.save(item1)
    json_inventory_repo.save(item2)
    json_inventory_repo.delete(item1.id)
    items = json_inventory_repo.get_all()

    assert len(items) == 1
    assert items[0].id == item2.id
