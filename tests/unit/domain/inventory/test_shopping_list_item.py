import math
from dataclasses import FrozenInstanceError

import pytest

from app.domain.inventory.shopping_list_item import ShoppingListItem


def test_create_valid_shopping_list_item():
    item = ShoppingListItem(name=" Milk ", quantity=2.0, unit=" l ")

    assert item.name == "Milk"
    assert item.quantity == 2.0
    assert item.unit == "l"


def test_create_shopping_list_item_converts_comma_string_quantity():
    item = ShoppingListItem(name="Butter", quantity="1,5", unit="kg")

    assert item.quantity == 1.5


def test_create_shopping_list_item_with_none_unit():
    item = ShoppingListItem(name="Salt", quantity=1.0, unit=None)  # type: ignore[arg-type]

    assert item.unit == ""


@pytest.mark.parametrize("invalid_quantity", [0.0, -1.5, "0", "-2,5"])
def test_shopping_list_item_raises_error_for_non_positive_quantity(invalid_quantity):
    with pytest.raises(ValueError, match="Ungültige Menge"):
        ShoppingListItem(name="Milk", quantity=invalid_quantity, unit="l")


@pytest.mark.parametrize(
    "invalid_quantity",
    ["invalid", math.nan, math.inf, -math.inf, None, []],
)
def test_shopping_list_item_raises_error_for_invalid_quantity_format(invalid_quantity):
    with pytest.raises(ValueError, match="Ungültige Menge"):
        ShoppingListItem(name="Milk", quantity=invalid_quantity, unit="l")  # type: ignore[arg-type]


@pytest.mark.parametrize("invalid_name", ["", "   ", None])
def test_shopping_list_item_raises_error_for_empty_name(invalid_name):
    with pytest.raises(ValueError, match="Ungültiger Name"):
        ShoppingListItem(name=invalid_name, quantity=1.0, unit="kg")  # type: ignore[arg-type]


def test_shopping_list_item_is_immutable():
    item = ShoppingListItem(name="Eggs", quantity=12.0, unit="pcs")

    with pytest.raises(FrozenInstanceError):
        item.quantity = 6.0  # type: ignore[misc]
