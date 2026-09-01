from uuid import UUID

from app.domain.inventory.shopping_list import ShoppingList
from app.domain.inventory.shopping_list_item import ShoppingListItem


def test_create_shopping_list_with_defaults():
    shopping_list = ShoppingList()

    assert isinstance(shopping_list.id, UUID)
    assert shopping_list.items == []


def test_create_shopping_list_with_custom_attributes():
    item = ShoppingListItem(name="Flour", quantity=1.0, unit="kg")
    shopping_list = ShoppingList(items=[item])

    assert len(shopping_list.items) == 1
    assert shopping_list.items[0] == item


def test_shopping_list_instances_have_unique_uuids_and_isolated_lists():
    list_1 = ShoppingList()
    list_2 = ShoppingList()

    assert list_1.id != list_2.id

    item = ShoppingListItem(name="Butter", quantity=250.0, unit="g")
    list_1.items.append(item)

    assert len(list_1.items) == 1
    assert len(list_2.items) == 0
