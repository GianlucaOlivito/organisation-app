from unittest.mock import MagicMock

import flet as ft

from app.domain.inventory.inventory_item import InventoryItem


def test_initialization_creation_mode(inventory_form):
    assert len(inventory_form._items_column.controls) == 1

    first_row = inventory_form._items_column.controls[0]

    assert first_row.controls[0].value == ""
    assert first_row.controls[1].value == ""
    assert first_row.controls[2].value == ""


def test_initialization_edit_mode(sample_items, inventory_form):
    inventory_form.__init__(inventory=sample_items)
    inventory_form.update = MagicMock()

    assert len(inventory_form._items_column.controls) == len(sample_items)

    first_row = inventory_form._items_column.controls[0]

    assert first_row.controls[0].value == sample_items[0].name
    assert first_row.controls[1].value == str(sample_items[0].quantity)
    assert first_row.controls[2].value == (sample_items[0].unit or "")


def test_add_item_row(inventory_form):
    initial_count = len(inventory_form._items_column.controls)
    inventory_form._add_item_row(name="Apple", quantity="5", unit="pcs")

    assert len(inventory_form._items_column.controls) == initial_count + 1

    new_row = inventory_form._items_column.controls[-1]

    assert isinstance(new_row, ft.Row)
    assert new_row.controls[0].value == "Apple"
    assert new_row.controls[1].value == "5"
    assert new_row.controls[2].value == "pcs"


def test_delete_item_row(inventory_form):
    inventory_form._add_item_row(name="Banana", quantity="3", unit="pcs")

    assert len(inventory_form._items_column.controls) == 2

    delete_button = inventory_form._items_column.controls[1].controls[3]
    delete_button.on_click(MagicMock())

    assert len(inventory_form._items_column.controls) == 1


def test_get_inventory_constructs_valid_domain_models(inventory_form):
    row = inventory_form._items_column.controls[0]
    row.controls[0].value = " Apple "
    row.controls[1].value = " 10 "
    row.controls[2].value = " kg "

    inventory = inventory_form.get_inventory()

    assert len(inventory) == 1
    assert isinstance(inventory[0], InventoryItem)
    assert inventory[0].name == "Apple"
    assert inventory[0].quantity == 10.0
    assert inventory[0].unit == "kg"


def test_get_inventory_filters_out_completely_empty_rows(inventory_form):
    row1 = inventory_form._items_column.controls[0]
    row1.controls[0].value = "Flour"
    row1.controls[1].value = "1000"
    row1.controls[2].value = "g"

    inventory_form._add_item_row(name="", quantity="", unit="")
    inventory = inventory_form.get_inventory()

    assert len(inventory) == 1
    assert inventory[0].name == "Flour"
    assert inventory[0].quantity == 1000.0


def test_handle_save_success(inventory_form):
    on_save_mock = MagicMock()
    inventory_form._on_save = on_save_mock

    row = inventory_form._items_column.controls[0]
    row.controls[0].value = "Milk"
    row.controls[1].value = "2"
    row.controls[2].value = "L"

    mock_event = MagicMock()
    inventory_form._handle_save(mock_event)

    assert inventory_form._error_text.visible is False
    on_save_mock.assert_called_once()

    saved_inventory = on_save_mock.call_args[0][0]

    assert len(saved_inventory) == 1
    assert saved_inventory[0].name == "Milk"


def test_handle_save_displays_error_on_validation_failure(inventory_form):
    on_save_mock = MagicMock()
    inventory_form._on_save = on_save_mock
    inventory_form.get_inventory = MagicMock(
        side_effect=ValueError("Name cannot be empty")
    )

    mock_event = MagicMock()
    inventory_form._handle_save(mock_event)

    assert inventory_form._error_text.visible is True
    assert inventory_form._error_text.value == "Name cannot be empty"
    on_save_mock.assert_not_called()
    inventory_form.update.assert_called_once()
