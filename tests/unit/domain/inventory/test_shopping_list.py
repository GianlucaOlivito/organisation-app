from uuid import UUID

import pytest

from app.domain.inventory.shopping_list import ShoppingList
from app.domain.inventory.shopping_list_item import ShoppingListItem


def test_create_valid_shopping_list():
    item = ShoppingListItem(name="Milk", quantity=2.0, unit="l")
    shopping_list = ShoppingList(items=[item])

    assert isinstance(shopping_list.id, UUID)
    assert len(shopping_list.items) == 1
    assert shopping_list.items[0] == item


def test_shopping_list_raises_error_when_items_list_is_empty():
    with pytest.raises(ValueError, match="Ungültige Einkaufsliste"):
        ShoppingList(items=[])


def test_shopping_list_instances_have_unique_uuids_and_isolated_lists():
    item1 = ShoppingListItem(name="Bread", quantity=1.0, unit="pc")
    item2 = ShoppingListItem(name="Butter", quantity=1.0, unit="pack")

    list_1 = ShoppingList(items=[item1])
    list_2 = ShoppingList(items=[item2])

    assert list_1.id != list_2.id

    extra_item = ShoppingListItem(name="Cheese", quantity=200.0, unit="g")
    list_1.items.append(extra_item)

    assert len(list_1.items) == 2
    assert len(list_2.items) == 1
