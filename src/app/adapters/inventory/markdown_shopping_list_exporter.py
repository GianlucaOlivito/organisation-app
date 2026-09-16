import logging
from pathlib import Path

from app.application.inventory.shopping_list_exporter import ShoppingListExporter
from app.domain.inventory.shopping_list import ShoppingList

logger = logging.getLogger(__name__)


class MarkdownShoppingListExporter(ShoppingListExporter):
    """Implementation of UC-3.4: Export Shopping List to a Markdown file."""

    def __init__(self) -> None:
        logger.debug("MarkdownShoppingListExporter initialized.")

    def export(self, shopping_list: ShoppingList, destination: Path) -> None:
        destination.parent.mkdir(parents=True, exist_ok=True)
        lines = [
            "# Einkaufsliste",
            "",
            "| Erledigt | Menge | Einheit | Artikel |",
            "| :---: | :---: | :---: | :--- |",
        ]
        for item in shopping_list.items:
            unit_str = f"{item.unit}" if item.unit else ""
            lines.append(f"| [ ] | {item.quantity} | {unit_str} | {item.name} |")
        content = "\n".join(lines) + "\n"
        destination.write_text(content, encoding="utf-8")
        logger.info("Exported shopping list to %s.", destination)
