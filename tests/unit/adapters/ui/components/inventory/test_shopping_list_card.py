import flet as ft

from app.adapters.ui.components.inventory.shopping_list_card import ShoppingListCard
from app.domain.inventory.shopping_list import ShoppingList


def test_shopping_list_card_renders_full_data(sample_shopping_list):
    card = ShoppingListCard(sample_shopping_list)

    assert isinstance(card, ft.Card)

    column = card.content.content

    assert isinstance(column, ft.Column)

    header_row = column.controls[0]

    assert header_row.controls[0].value == "Einkaufsliste"

    sl_section = column.controls[2]

    assert isinstance(sl_section, ft.Column)
    assert len(sl_section.controls) == len(sample_shopping_list.items)

    for i, item in enumerate(sample_shopping_list.items):
        row = sl_section.controls[i]

        assert isinstance(row, ft.Row)

        qty_control = row.controls[0]
        name_control = row.controls[1]
        qty = int(item.quantity) if item.quantity.is_integer() else item.quantity
        unit_str = item.unit if item.unit else ""

        assert qty_control.value == f"{qty} {unit_str}".strip()
        assert name_control.value == item.name


def test_shopping_list_card_callbacks_trigger(sample_shopping_list):
    applied_list = None
    export_called = False
    clear_called = False

    def on_apply(sl: ShoppingList) -> None:
        nonlocal applied_list
        applied_list = sl

    def on_export() -> None:
        nonlocal export_called
        export_called = True

    def on_clear() -> None:
        nonlocal clear_called
        clear_called = True

    card = ShoppingListCard(
        sample_shopping_list,
        on_apply=on_apply,
        on_export=on_export,
        on_clear=on_clear,
    )
    header_row = card.content.content.controls[0]
    action_row = header_row.controls[1]
    apply_btn = action_row.controls[0]
    export_btn = action_row.controls[1]
    clear_btn = action_row.controls[2]
    apply_btn.on_click(None)

    assert applied_list == sample_shopping_list

    export_btn.on_click(None)

    assert export_called is True

    clear_btn.on_click(None)

    assert clear_called is True
