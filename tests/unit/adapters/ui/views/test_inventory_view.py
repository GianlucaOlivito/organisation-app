from unittest.mock import MagicMock

import flet as ft

from app.adapters.ui.components.inventory.inventory_card import InventoryCard
from app.adapters.ui.components.inventory.inventory_form import InventoryForm
from app.domain.inventory.inventory_item import InventoryItem


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
    toolbar = inventory_view._toolbar

    assert isinstance(toolbar, ft.Row)
    assert len(toolbar.controls) == 3
    assert toolbar.controls[0] == inventory_view._add_button
    assert toolbar.controls[1] == inventory_view._search_button
    assert toolbar.controls[2] == inventory_view._search_input


def test_open_form_renders_inventory_form(inventory_view):
    inventory_view._open_form()

    assert inventory_view._toolbar.visible is False
    assert len(inventory_view._content_container.controls) == 1
    assert isinstance(inventory_view._content_container.controls[0], InventoryForm)


def test_close_form_restores_toolbar_and_renders_results(inventory_view):
    inventory_view._open_form()
    inventory_view._close_form()

    assert inventory_view._toolbar.visible is True
    assert isinstance(inventory_view._content_container.controls[0], InventoryCard)


def test_save_form_creates_modifies_and_deletes_items(
    inventory_view, inventory_modification_service, sample_items
):
    inventory_modification_service.create = MagicMock()
    inventory_modification_service.modify = MagicMock()
    inventory_modification_service.delete = MagicMock()
    modified_item = sample_items[0]
    new_item = InventoryItem(name="Zucker", quantity=500, unit="g")
    inventory_view._open_form(entity=sample_items)
    form = inventory_view._content_container.controls[0]
    form._on_save([modified_item, new_item])

    inventory_modification_service.modify.assert_called_once_with(modified_item)
    inventory_modification_service.create.assert_called_once_with(new_item)
    inventory_modification_service.delete.assert_called_once_with(sample_items[1].id)
    assert inventory_view._toolbar.visible is True


def test_refresh_triggers_search(inventory_view, sample_items):
    target_item = sample_items[0]
    inventory_view._search_input.value = target_item.name
    inventory_view.refresh()
    card = inventory_view._content_container.controls[0]

    assert isinstance(card, InventoryCard)
    assert len(card.inventory) == 1
    assert card.inventory[0].name == target_item.name
