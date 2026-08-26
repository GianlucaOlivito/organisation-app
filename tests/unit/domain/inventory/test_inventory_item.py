from uuid import UUID

import pytest

from app.domain.inventory.inventory_item import InventoryItem


def test_create_valid_inventory_item() -> None:
    inventory_item = InventoryItem(name="Flour", quantity=500.0, unit="g")

    assert inventory_item.name == "Flour"
    assert inventory_item.quantity == 500.0
    assert inventory_item.unit == "g"


def test_create_inventory_item_with_empty_unit() -> None:
    inventory_item = InventoryItem(name="Egg", quantity=12.0, unit="")

    assert inventory_item.unit == ""


def test_inventory_item_generates_unique_uuid() -> None:
    item_1 = InventoryItem(name="Apple", quantity=5.0, unit="")
    item_2 = InventoryItem(name="Apple", quantity=5.0, unit="")

    assert isinstance(item_1.id, UUID)
    assert item_1.id != item_2.id


def test_inventory_item_raises_error_for_negative_quantity() -> None:
    with pytest.raises(
        ValueError, match="INVALID ARGUMENT: Item quantity cannot be negative."
    ):
        InventoryItem(name="Sugar", quantity=-50.0, unit="g")


@pytest.mark.parametrize("invalid_name", ["", "   "])
def test_inventory_item_raises_error_for_empty_name(invalid_name: str) -> None:
    with pytest.raises(
        ValueError, match="INVALID ARGUMENT: Item name cannot be empty."
    ):
        InventoryItem(name=invalid_name, quantity=100.0, unit="g")
