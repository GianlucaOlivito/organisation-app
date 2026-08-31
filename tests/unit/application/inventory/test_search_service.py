from uuid import uuid4

import pytest

from app.application.inventory.search_service import InventorySearchService
from app.domain.inventory.inventory_item import InventoryItem


@pytest.fixture
def search_service(fake_inventory_repo) -> InventorySearchService:
    return InventorySearchService(inventory_repository=fake_inventory_repo)


@pytest.fixture
def sample_items(fake_inventory_repo) -> list[InventoryItem]:
    item1 = InventoryItem(id=uuid4(), name="Milk", quantity=2.0, unit="l")
    item2 = InventoryItem(id=uuid4(), name="Eggs", quantity=12.0, unit="")
    fake_inventory_repo.save(item1)
    fake_inventory_repo.save(item2)
    return [item1, item2]


def test_get_all_returns_empty_list_when_no_items(search_service):
    assert search_service.get_all() == []


def test_get_all_returns_all_inventory_items(search_service, sample_items):
    results = search_service.get_all()
    assert len(results) == 2
    assert results == sample_items


def test_get_by_id_returns_item_when_found(search_service, sample_items):
    expected_item = sample_items[0]
    found_item = search_service.get_by_id(expected_item.id)
    assert found_item == expected_item


def test_get_by_id_returns_none_when_not_found(search_service):
    assert search_service.get_by_id(uuid4()) is None


def test_get_by_name_returns_item_when_found(search_service, sample_items):
    expected_item = sample_items[0]
    found_item = search_service.get_by_name(expected_item.name)
    assert found_item == expected_item


def test_get_by_name_returns_none_when_not_found(search_service):
    assert search_service.get_by_name("Chocolate") is None
