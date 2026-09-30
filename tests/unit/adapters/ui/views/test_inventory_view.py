import flet as ft

from app.adapters.ui.components.inventory.inventory_card import InventoryCard


def test_initialization_renders_sample_items(inventory_view, sample_items):
    card = inventory_view._content_container.controls[0]

    assert len(inventory_view._content_container.controls) == 1
    assert isinstance(card, InventoryCard)
    assert card.inventory == sample_items


def test_search_by_name(inventory_view, sample_items):
    target_item = sample_items[0]
    inventory_view._search_input.value = target_item.name
    inventory_view._search()
    card = inventory_view._content_container.controls[0]

    assert isinstance(card, InventoryCard)
    assert len(card.inventory) == 1
    assert card.inventory[0].name == target_item.name


def test_search_by_id(inventory_view, sample_items):
    target_item = sample_items[0]
    inventory_view._search_input.value = str(target_item.id)
    inventory_view._search()
    card = inventory_view._content_container.controls[0]

    assert isinstance(card, InventoryCard)
    assert len(card.inventory) == 1
    assert card.inventory[0].id == target_item.id


def test_search_empty_state_when_no_match(inventory_view):
    inventory_view._search_input.value = "Non Existent Item"
    inventory_view._search()

    assert inventory_view._content_container.controls == [inventory_view._empty_state]


def test_toolbar_structure(inventory_view):
    toolbar = inventory_view.controls[2]

    assert isinstance(toolbar, ft.Row)
    assert len(toolbar.controls) == 2
    assert toolbar.controls[0] == inventory_view._search_button
    assert toolbar.controls[1] == inventory_view._search_input
