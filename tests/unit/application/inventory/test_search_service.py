from uuid import uuid4


def test_get_all_returns_empty_list_when_no_items(inventory_search_service):
    assert inventory_search_service.get_all() == []


def test_get_all_returns_all_inventory_items(inventory_search_service, sample_items):
    results = inventory_search_service.get_all()

    assert len(results) == 2
    assert results == sample_items


def test_get_by_id_returns_item_when_found(inventory_search_service, sample_items):
    expected_item = sample_items[0]
    found_item = inventory_search_service.get_by_id(expected_item.id)

    assert found_item == expected_item


def test_get_by_id_returns_none_when_not_found(inventory_search_service):
    assert inventory_search_service.get_by_id(uuid4()) is None


def test_get_by_name_returns_item_when_found(inventory_search_service, sample_items):
    expected_item = sample_items[0]
    found_item = inventory_search_service.get_by_name(expected_item.name)

    assert found_item == expected_item


def test_get_by_name_returns_none_when_not_found(inventory_search_service):
    assert inventory_search_service.get_by_name("Chocolate") is None
