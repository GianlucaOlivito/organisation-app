from app.domain.inventory.shopping_list import ShoppingList
from app.domain.inventory.shopping_list_item import ShoppingListItem


def test_export_creates_markdown_file_with_table(tmp_path, markdown_exporter):
    destination = tmp_path / "shopping_list.md"
    shopping_list = ShoppingList(
        items=[
            ShoppingListItem(name="Milk", quantity=2, unit="l"),
            ShoppingListItem(name="Eggs", quantity=6, unit=""),
        ],
    )
    markdown_exporter.export(shopping_list, destination)

    assert destination.exists()

    content = destination.read_text(encoding="utf-8")

    assert "# Einkaufsliste" in content
    assert "| Erledigt | Menge | Einheit | Artikel |" in content
    assert "| [ ] | 2.0 | l | Milk |" in content
    assert "| [ ] | 6.0 |  | Eggs |" in content


def test_export_creates_nested_parent_directories(tmp_path, markdown_exporter):
    destination = tmp_path / "nested" / "exports" / "shopping_list.md"
    item = ShoppingListItem(name="Milk", quantity=2, unit="l")
    shopping_list = ShoppingList(items=[item])
    markdown_exporter.export(shopping_list, destination)

    assert destination.exists()
