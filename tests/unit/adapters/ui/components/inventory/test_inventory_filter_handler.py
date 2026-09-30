def test_filter_returns_all_when_no_inputs(inventory_filter_handler, sample_items):
    result = inventory_filter_handler.filter()

    assert result == sample_items


def test_filter_by_valid_id(inventory_filter_handler, sample_items):
    target = sample_items[0]
    result = inventory_filter_handler.filter(query=str(target.id))

    assert result == [target]


def test_filter_by_invalid_id_returns_empty(inventory_filter_handler):
    result = inventory_filter_handler.filter(query="invalid-uuid")

    assert result == []


def test_filter_by_valid_name(inventory_filter_handler, sample_items):
    target = sample_items[0]
    result = inventory_filter_handler.filter(query=target.name)

    assert result == [target]


def test_filter_by_invalid_name_returns_empty(inventory_filter_handler):
    result = inventory_filter_handler.filter(query="NonExistentItem")

    assert result == []


def test_filter_with_whitespace_query(inventory_filter_handler, sample_items):
    target = sample_items[0]
    result = inventory_filter_handler.filter(query=f"  {target.name}  ")

    assert result == [target]
