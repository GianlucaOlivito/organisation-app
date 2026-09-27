import math
from uuid import UUID

import pytest

from app.domain.inventory.inventory_item import InventoryItem


def test_create_valid_inventory_item():
    inventory_item = InventoryItem(name=" Flour ", quantity=500.0, unit=" g ")

    assert inventory_item.name == "Flour"
    assert inventory_item.quantity == 500.0
    assert inventory_item.unit == "g"


def test_create_inventory_item_converts_comma_string_quantity():
    inventory_item = InventoryItem(name="Sugar", quantity="12,5", unit="kg")

    assert inventory_item.quantity == 12.5


def test_create_inventory_item_with_empty_or_none_unit():
    item1 = InventoryItem(name="Egg", quantity=12.0, unit="")
    item2 = InventoryItem(name="Egg", quantity=12.0, unit=None)  # type: ignore[arg-type]

    assert item1.unit == ""
    assert item2.unit == ""


def test_inventory_item_generates_unique_uuid():
    item_1 = InventoryItem(name="Apple", quantity=5.0, unit="")
    item_2 = InventoryItem(name="Apple", quantity=5.0, unit="")

    assert isinstance(item_1.id, UUID)
    assert item_1.id != item_2.id


@pytest.mark.parametrize("invalid_qty", [-50.0, -0.1, "-10,0"])
def test_inventory_item_raises_error_for_negative_quantity(invalid_qty):
    with pytest.raises(ValueError, match="Ungültige Menge"):
        InventoryItem(name="Sugar", quantity=invalid_qty, unit="g")


@pytest.mark.parametrize(
    "invalid_qty",
    ["invalid", math.nan, math.inf, -math.inf, None, []],
)
def test_inventory_item_raises_error_for_invalid_quantity_type(invalid_qty):
    with pytest.raises(ValueError, match="Ungültige Menge"):
        InventoryItem(name="Sugar", quantity=invalid_qty, unit="g")  # type: ignore[arg-type]


@pytest.mark.parametrize("invalid_name", ["", "   ", None])
def test_inventory_item_raises_error_for_empty_name(invalid_name):
    with pytest.raises(ValueError, match="Ungültiger Name"):
        InventoryItem(name=invalid_name, quantity=100.0, unit="g")  # type: ignore[arg-type]
