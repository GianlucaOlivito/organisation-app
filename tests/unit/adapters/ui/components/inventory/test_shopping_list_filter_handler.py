from unittest.mock import MagicMock

from app.adapters.ui.components.inventory.shopping_list_filter_handler import (
    ShoppingListFilterHandler,
)
from app.application.inventory.shopping_list_service import ShoppingListService


def test_filter_returns_none_when_no_inputs(shopping_list_filter_handler):
    result = shopping_list_filter_handler.filter()

    assert result is None


def test_filter_returns_none_when_missing_start_or_end_date(
    shopping_list_filter_handler,
):
    assert shopping_list_filter_handler.filter(start_date="01.09.2026") is None
    assert shopping_list_filter_handler.filter(end_date="05.09.2026") is None


def test_filter_by_inclusive_date_range(
    shopping_list_filter_handler, sample_menus, sample_items
):
    result = shopping_list_filter_handler.filter(
        start_date="01.09.2026", end_date="05.09.2026"
    )

    assert result is not None
    assert len(result.items) == 1
    assert result.items[0].name == "Pasta"
    assert result.items[0].quantity == 400.0
    assert result.items[0].unit == "g"


def test_filter_by_invalid_date_returns_none(shopping_list_filter_handler):
    result = shopping_list_filter_handler.filter(
        start_date="not-a-date", end_date="01.09.2026"
    )

    assert result is None


def test_filter_returns_none_for_inverted_date_range(
    shopping_list_filter_handler,
):
    result = shopping_list_filter_handler.filter(
        start_date="10.09.2026", end_date="01.09.2026"
    )

    assert result is None


def test_filter_handles_service_value_error_gracefully():
    mock_service = MagicMock(spec=ShoppingListService)
    mock_service.generate_shopping_list.side_effect = ValueError(
        "Ungültige Einkaufsliste"
    )
    handler = ShoppingListFilterHandler(mock_service)
    result = handler.filter(start_date="01.09.2026", end_date="05.09.2026")

    assert result is None
