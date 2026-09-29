from unittest.mock import MagicMock
from uuid import UUID, uuid4

import flet as ft

from app.adapters.ui.components.meal_planning.menu_card import MenuCard
from app.application.recipes.search_service import RecipeSearchService
from app.domain.meal_planning.course import Course
from app.domain.meal_planning.menu import Menu


def test_format_course_quantities_and_grammar():
    assert (
        MenuCard._format_course(1, "Spaghetti Carbonara")
        == "• 1 Portion Spaghetti Carbonara"
    )
    assert MenuCard._format_course(2, "Tomato Soup") == "• 2 Portionen Tomato Soup"


def test_menu_card_renders_full_data(sample_menus, sample_recipes):
    menu = sample_menus[0]
    valid_recipe = sample_recipes[0]
    missing_recipe_id = uuid4()
    menu.courses.append(Course(recipe_id=missing_recipe_id, portions=1))
    mock_search_service = MagicMock(spec=RecipeSearchService)

    def side_effect(rid: UUID):
        if rid == valid_recipe.id:
            return valid_recipe
        return None

    mock_search_service.get_by_id.side_effect = side_effect
    card = MenuCard(menu, recipe_search_service=mock_search_service)

    assert isinstance(card, ft.Card)

    column = card.content.content

    assert isinstance(column, ft.Column)

    header_row = column.controls[0]
    expected_header_text = "Lunch, 01.09.2026"

    assert header_row.controls[0].value == expected_header_text
    assert header_row.controls[1].controls[0].value == f"ID: {str(menu.id)[:8]}"

    courses_section = column.controls[2]

    assert courses_section.controls[0].value == "Gänge"
    assert len(courses_section.controls) == 3
    assert courses_section.controls[1].value == f"• 2 Portionen {valid_recipe.name}"
    assert courses_section.controls[2].value == "• 1 Portion Unbekanntes Rezept"


def test_menu_card_callback_triggers(sample_menus):
    menu = sample_menus[0]
    mock_search_service = MagicMock(spec=RecipeSearchService)
    edited_menu = None
    deleted_id = None

    def on_edit(m: Menu) -> None:
        nonlocal edited_menu
        edited_menu = m

    def on_delete(mid: UUID) -> None:
        nonlocal deleted_id
        deleted_id = mid

    card = MenuCard(
        menu,
        recipe_search_service=mock_search_service,
        on_edit=on_edit,
        on_delete=on_delete,
    )
    header_row = card.content.content.controls[0]
    action_row = header_row.controls[1]
    edit_btn = action_row.controls[1]
    delete_btn = action_row.controls[2]
    edit_btn.on_click(None)

    assert edited_menu == menu

    delete_btn.on_click(None)

    assert deleted_id == menu.id
