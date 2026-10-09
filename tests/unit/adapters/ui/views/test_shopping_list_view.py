from dataclasses import replace
from datetime import date
from unittest.mock import MagicMock

from app.domain.inventory.shopping_list import ShoppingList
from app.domain.inventory.shopping_list_item import ShoppingListItem
from app.domain.meal_planning.course import Course
from app.domain.meal_planning.menu import Menu
from app.domain.recipes.recipe import Recipe
from app.domain.recipes.recipe_ingredient import RecipeIngredient


def test_shopping_list_view_initialization_renders_empty_state(shopping_list_view):
    assert shopping_list_view._start_date_input.value == ""
    assert shopping_list_view._end_date_input.value == ""
    assert len(shopping_list_view._content_container.controls) == 1
    assert (
        shopping_list_view._content_container.controls[0]
        == shopping_list_view._empty_state
    )


def test_generate_shopping_list_renders_card_when_items_exist(
    shopping_list_view,
    fake_recipe_repo,
    fake_menu_repo,
):
    recipe = Recipe(
        name="Pancakes",
        ingredients=[RecipeIngredient(name="Flour", quantity=500.0, unit="g")],
        instructions="Mix and fry.",
    )
    fake_recipe_repo.save(recipe)
    fake_menu_repo.save(
        Menu(
            description="Breakfast",
            scheduled_date=date(2026, 9, 1),
            courses=[Course(recipe_id=recipe.id, portions=1)],
        )
    )
    shopping_list_view._start_date_input.value = "01.09.2026"
    shopping_list_view._end_date_input.value = "02.09.2026"
    shopping_list_view._generate_shopping_list_button.on_click(None)

    assert shopping_list_view._shopping_list is not None
    assert len(shopping_list_view._shopping_list.items) == 1
    assert shopping_list_view.update.called


def test_generate_shopping_list_clears_view_when_no_items_needed(shopping_list_view):
    shopping_list_view._start_date_input.value = "01.09.2026"
    shopping_list_view._end_date_input.value = "02.09.2026"
    shopping_list_view._generate_shopping_list_button.on_click(None)

    assert shopping_list_view._shopping_list is None
    assert shopping_list_view._content_container.controls == [
        shopping_list_view._empty_state
    ]
    assert shopping_list_view.update.called


def test_handle_consume_meals_calls_reconciliation_service(
    shopping_list_view,
    inventory_reconciliation_service,
):
    spy_consume = MagicMock(
        side_effect=inventory_reconciliation_service.consume_meals_for_period
    )
    inventory_reconciliation_service.consume_meals_for_period = spy_consume
    shopping_list_view._start_date_input.value = "01.09.2026"
    shopping_list_view._end_date_input.value = "05.09.2026"
    shopping_list_view._consume_meals_button.on_click(None)

    spy_consume.assert_called_once_with(
        start_date=date(2026, 9, 1),
        end_date=date(2026, 9, 5),
    )


def test_handle_consume_meals_ignores_invalid_dates(
    shopping_list_view,
    inventory_reconciliation_service,
):
    spy_consume = MagicMock()
    inventory_reconciliation_service.consume_meals_for_period = spy_consume
    shopping_list_view._start_date_input.value = "invalid-date"
    shopping_list_view._end_date_input.value = "05.09.2026"
    shopping_list_view._consume_meals_button.on_click(None)

    spy_consume.assert_not_called()


def test_handle_apply_shopping_list_applies_and_clears_list(
    shopping_list_view,
    inventory_reconciliation_service,
):
    spy_apply = MagicMock(
        side_effect=inventory_reconciliation_service.apply_shopping_list
    )
    inventory_reconciliation_service.apply_shopping_list = spy_apply
    shopping_list = ShoppingList(
        items=[ShoppingListItem(name="Butter", quantity=250.0, unit="g")]
    )
    shopping_list_view._handle_apply_shopping_list(shopping_list)

    spy_apply.assert_called_once_with(shopping_list)
    assert shopping_list_view._shopping_list is None
    assert shopping_list_view._content_container.controls == [
        shopping_list_view._empty_state
    ]
    assert shopping_list_view.update.called


def test_clear_list_resets_content_container_and_state(shopping_list_view):
    shopping_list_view._shopping_list = ShoppingList(
        items=[ShoppingListItem(name="Eggs", quantity=6.0, unit="pcs")]
    )
    shopping_list_view._clear_list()

    assert shopping_list_view._shopping_list is None
    assert shopping_list_view._content_container.controls == [
        shopping_list_view._empty_state
    ]
    assert shopping_list_view.update.called


def test_handle_export_shopping_list_exports_when_list_exists(
    shopping_list_view, tmp_path
):
    export_file = tmp_path / "shopping_list.md"
    shopping_list_view._settings = replace(
        shopping_list_view._settings, shopping_list_file_path=export_file
    )
    shopping_list = ShoppingList(
        items=[ShoppingListItem(name="Milch", quantity=1.0, unit="l")]
    )
    shopping_list_view._shopping_list = shopping_list
    shopping_list_view._handle_export_shopping_list()

    assert export_file.exists()
    assert "Milch" in export_file.read_text(encoding="utf-8")


def test_handle_export_shopping_list_does_nothing_when_no_list(
    shopping_list_view, tmp_path
):
    export_file = tmp_path / "shopping_list.md"
    shopping_list_view._settings = replace(
        shopping_list_view._settings, shopping_list_file_path=export_file
    )
    shopping_list_view._shopping_list = None
    shopping_list_view._handle_export_shopping_list()

    assert not export_file.exists()
