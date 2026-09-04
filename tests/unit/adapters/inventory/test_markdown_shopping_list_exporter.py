import pytest

from app.adapters.inventory.markdown_shopping_list_exporter import (
    MarkdownShoppingListExporter,
)
from app.domain.inventory.shopping_list import ShoppingList, ShoppingListItem


@pytest.fixture
def exporter() -> MarkdownShoppingListExporter:
    return MarkdownShoppingListExporter()


def test_export_creates_markdown_file_with_table(tmp_path, exporter):
    destination = tmp_path / "shopping_list.md"
    shopping_list = ShoppingList(
        items=[
            ShoppingListItem(name="Milk", quantity=2, unit="l"),
            ShoppingListItem(name="Eggs", quantity=6, unit=""),
        ],
    )
    exporter.export(shopping_list, destination)

    assert destination.exists()

    content = destination.read_text(encoding="utf-8")

    assert "# Einkaufsliste" in content
    assert "| Erledigt | Menge | Einheit | Artikel |" in content
    assert "| [ ] | 2 | l | Milk |" in content
    assert "| [ ] | 6 |  | Eggs |" in content


def test_export_creates_nested_parent_directories(tmp_path, exporter):
    destination = tmp_path / "nested" / "exports" / "shopping_list.md"
    shopping_list = ShoppingList(items=[])
    exporter.export(shopping_list, destination)

    assert destination.exists()


def test_export_empty_shopping_list(tmp_path, exporter):
    destination = tmp_path / "empty.md"
    shopping_list = ShoppingList(items=[])
    exporter.export(shopping_list, destination)
    content = destination.read_text(encoding="utf-8")
    lines = content.strip().split("\n")

    assert lines[0] == "# Einkaufsliste"
    assert len(lines) == 4  # Header, blank line, 2 table header lines
