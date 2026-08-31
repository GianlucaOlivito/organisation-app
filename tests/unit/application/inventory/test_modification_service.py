from uuid import uuid4

import pytest

from app.application.inventory.modification_service import InventoryModificationService
from app.domain.inventory.inventory_item import InventoryItem


@pytest.fixture
def modification_service(fake_inventory_repo) -> InventoryModificationService:
    return InventoryModificationService(inventory_repository=fake_inventory_repo)


@pytest.fixture
def sample_item() -> InventoryItem:
    return InventoryItem(id=uuid4(), name="Milk", quantity=2.0, unit="l")


def test_create_inventory_item_success(
    modification_service, fake_inventory_repo, sample_item
):
    created_item = modification_service.create(sample_item)

    assert created_item == sample_item
    assert fake_inventory_repo.get_by_id(sample_item.id) == sample_item


def test_create_inventory_item_already_exists_raises_error(
    modification_service, fake_inventory_repo, sample_item
):
    fake_inventory_repo.save(sample_item)

    with pytest.raises(
        ValueError,
        match=f"INVALID ARGUMENT: Inventory item with ID '{sample_item.id}' already exists.",
    ):
        modification_service.create(sample_item)


def test_modify_inventory_item_success(
    modification_service, fake_inventory_repo, sample_item
):
    fake_inventory_repo.save(sample_item)
    updated_item = InventoryItem(
        id=sample_item.id, name=sample_item.name, quantity=5.0, unit="l"
    )
    modification_service.modify(updated_item)
    saved_item = fake_inventory_repo.get_by_id(sample_item.id)

    assert saved_item is not None
    assert saved_item.quantity == 5.0


def test_modify_inventory_item_not_found_raises_error(
    modification_service, sample_item
):
    with pytest.raises(
        ValueError,
        match=f"INVALID ARGUMENT: Inventory item with ID '{sample_item.id}' does not exist.",
    ):
        modification_service.modify(sample_item)


def test_delete_inventory_item_success(
    modification_service, fake_inventory_repo, sample_item
):
    fake_inventory_repo.save(sample_item)
    modification_service.delete(sample_item.id)

    assert fake_inventory_repo.get_by_id(sample_item.id) is None


def test_delete_inventory_item_not_found_raises_error(modification_service):
    non_existent_id = uuid4()
    with pytest.raises(
        ValueError,
        match=f"INVALID ARGUMENT: Inventory item with ID '{non_existent_id}' does not exist.",
    ):
        modification_service.delete(non_existent_id)
