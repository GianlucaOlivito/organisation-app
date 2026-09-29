def test_filter_returns_all_when_no_inputs(menu_filter_handler, sample_menus):
    result = menu_filter_handler.filter()

    assert result == sample_menus


def test_filter_by_valid_id(menu_filter_handler, sample_menus):
    target = sample_menus[0]
    result = menu_filter_handler.filter(query=str(target.id))

    assert result == [target]


def test_filter_by_invalid_id_returns_empty(menu_filter_handler):
    result = menu_filter_handler.filter(query="invalid-uuid")

    assert result == []


def test_filter_by_inclusive_date_range(menu_filter_handler, sample_menus):
    result = menu_filter_handler.filter(start_date="01.09.2026", end_date="05.09.2026")

    assert result == [sample_menus[0]]


def test_filter_by_single_date_bound(menu_filter_handler, sample_menus):
    result_start = menu_filter_handler.filter(start_date="05.09.2026")

    assert result_start == [sample_menus[1]]

    result_end = menu_filter_handler.filter(end_date="05.09.2026")

    assert result_end == [sample_menus[0]]
