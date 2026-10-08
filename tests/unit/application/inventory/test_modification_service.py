from dataclasses import replace
from uuid import uuid4

import pytest

from app.domain.inventory.inventory_item import InventoryItem


def test_create_inventory_item_success(
    inventory_modification_service, fake_inventory_repo
):
    item = InventoryItem(name="Milk", quantity=2.0, unit="l")
    created_item = inventory_modification_service.create(item)

    assert created_item.name == "Milk"
    assert created_item.quantity == 2000.0
    assert created_item.unit == "ml"


def test_create_inventory_item_merges_with_existing(
    inventory_modification_service, sample_items
):
    new_item = InventoryItem(name="Milk", quantity=1.0, unit="l")
    result = inventory_modification_service.create(new_item)

    assert result.id == sample_items[0].id
    assert result.quantity == 3000.0
    assert result.unit == "ml"


def test_modify_inventory_item_success(
    inventory_modification_service, fake_inventory_repo, sample_items
):
    sample_item = sample_items[0]
    updated_item = replace(sample_item, quantity=5.0)
    inventory_modification_service.modify(updated_item)
    saved_item = fake_inventory_repo.get_by_id(sample_item.id)

    assert saved_item is not None
    assert saved_item.quantity == 5.0


def test_modify_inventory_item_not_found_raises_error(inventory_modification_service):
    unregistered_item = InventoryItem(name="Unsaved Stock", quantity=1.0, unit="kg")

    with pytest.raises(
        ValueError,
        match=f"INVALID ARGUMENT: Inventory item with ID '{unregistered_item.id}' does not exist.",
    ):
        inventory_modification_service.modify(unregistered_item)


def test_delete_inventory_item_success(
    inventory_modification_service, fake_inventory_repo, sample_items
):
    sample_item = sample_items[0]
    inventory_modification_service.delete(sample_item.id)

    assert fake_inventory_repo.get_by_id(sample_item.id) is None


def test_delete_inventory_item_not_found_raises_error(inventory_modification_service):
    non_existent_id = uuid4()

    with pytest.raises(
        ValueError,
        match=f"INVALID ARGUMENT: Inventory item with ID '{non_existent_id}' does not exist.",
    ):
        inventory_modification_service.delete(non_existent_id)
