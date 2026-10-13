import flet as ft

from app.adapters.ui.components.inventory.inventory_card import InventoryCard


def test_inventory_card_renders_full_data(sample_items):
    card = InventoryCard(sample_items)

    assert isinstance(card, ft.Card)

    column = card.content.content

    assert isinstance(column, ft.Column)

    header_row = column.controls[0]

    assert header_row.controls[0].value == "Vorrat"

    inv_section = column.controls[2]

    assert isinstance(inv_section, ft.Column)
    assert len(inv_section.controls) == len(sample_items)

    for i, item in enumerate(sample_items):
        row = inv_section.controls[i]

        assert isinstance(row, ft.Row)

        id_control = row.controls[0]
        qty_control = row.controls[1]
        name_control = row.controls[2]
        qty = int(item.quantity) if item.quantity.is_integer() else item.quantity
        unit_str = f" {item.unit}" if item.unit else ""

        assert id_control.value == str(item.id)[:8]
        assert qty_control.value == f"{qty}{unit_str}".strip()
        assert name_control.value == item.name


def test_inventory_card_callback_triggers(sample_items):
    item = sample_items[0]
    inventory = [item]
    edited_inventory = None

    def on_edit(inventory) -> None:
        nonlocal edited_inventory
        edited_inventory = inventory

    card = InventoryCard(inventory, on_edit=on_edit)
    header_row = card.content.content.controls[0]
    right_row = header_row.controls[1]
    edit_btn = right_row.controls[0]
    edit_btn.on_click(None)

    assert edited_inventory == inventory
