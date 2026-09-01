from dataclasses import FrozenInstanceError

import pytest

from app.domain.inventory.shopping_list_item import ShoppingListItem


def test_create_valid_shopping_list_item():
    item = ShoppingListItem(name="Milk", quantity=2.0, unit="l")

    assert item.name == "Milk"
    assert item.quantity == 2.0
    assert item.unit == "l"


@pytest.mark.parametrize("invalid_quantity", [0.0, -1.5])
def test_shopping_list_item_raises_error_for_non_positive_quantity(
    invalid_quantity: float,
):
    with pytest.raises(
        ValueError, match="INVALID ARGUMENT: Item quantity must be positive."
    ):
        ShoppingListItem(name="Milk", quantity=invalid_quantity, unit="l")


@pytest.mark.parametrize("invalid_name", ["", "   "])
def test_shopping_list_item_raises_error_for_empty_name(invalid_name: str):
    with pytest.raises(
        ValueError, match="INVALID ARGUMENT: Item name cannot be empty."
    ):
        ShoppingListItem(name=invalid_name, quantity=1.0, unit="kg")


def test_shopping_list_item_is_immutable():
    item = ShoppingListItem(name="Eggs", quantity=12.0, unit="pcs")

    with pytest.raises(FrozenInstanceError):
        item.quantity = 6.0  # type: ignore[misc]
