import flet as ft

from app.adapters.ui.components.inventory.inventory_card import InventoryCard
from app.domain.inventory.inventory_item import InventoryItem


def test_format_inventory_item():
    item_whole = InventoryItem(name="Eier", quantity=10.0, unit="")
    item_unit = InventoryItem(name="Mehl", quantity=500.0, unit="g")
    item_decimal = InventoryItem(name="Milch", quantity=1.5, unit="l")
    formatted_whole = InventoryCard._format_inventory_item(item_whole)
    formatted_unit = InventoryCard._format_inventory_item(item_unit)
    formatted_decimal = InventoryCard._format_inventory_item(item_decimal)
    id_whole = str(item_whole.id)[:8]
    id_unit = str(item_unit.id)[:8]
    id_decimal = str(item_decimal.id)[:8]

    assert formatted_whole == f"{id_whole:<10} {'10'.ljust(12)} Eier"
    assert formatted_unit == f"{id_unit:<10} {'500  g'.ljust(12)} Mehl"
    assert formatted_decimal == f"{id_decimal:<10} {'1.5  l'.ljust(12)} Milch"


def test_inventory_card_renders_full_data():
    item1 = InventoryItem(name="Mehl", quantity=500.0, unit="g")
    item2 = InventoryItem(name="Milch", quantity=1.0, unit="l")
    inventory = [item1, item2]
    card = InventoryCard(inventory)

    assert isinstance(card, ft.Card)

    column = card.content.content

    assert isinstance(column, ft.Column)

    header_row = column.controls[0]

    assert header_row.controls[0].value == "Vorrat"

    inv_section = column.controls[2]

    assert isinstance(inv_section, ft.Column)
    assert len(inv_section.controls) == len(inventory)

    for i, item in enumerate(inventory):
        row = inv_section.controls[i]
        assert isinstance(row, ft.Row)
        assert row.controls[0].value == InventoryCard._format_inventory_item(item)


def test_inventory_card_callback_triggers():
    item = InventoryItem(name="Zucker", quantity=1.0, unit="kg")
    inventory = [item]
    edited_inventory = None

    def on_edit(inv: list[InventoryItem]) -> None:
        nonlocal edited_inventory
        edited_inventory = inv

    card = InventoryCard(inventory, on_edit=on_edit)
    header_row = card.content.content.controls[0]
    edit_btn = header_row.controls[1]
    edit_btn.on_click(None)

    assert edited_inventory == inventory
