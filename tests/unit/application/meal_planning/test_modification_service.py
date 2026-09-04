from dataclasses import replace
from datetime import date
from uuid import uuid4

import pytest

from app.domain.meal_planning.menu import Menu


def test_create_menu_success(meal_planning_modification_service, fake_menu_repo):
    menu = Menu(scheduled_date=date(2026, 8, 30), description="Lunch", courses=[])
    created_menu = meal_planning_modification_service.create(menu)

    assert created_menu == menu
    assert fake_menu_repo.get_by_id(menu.id) == menu


def test_create_menu_already_exists_raises_error(
    meal_planning_modification_service, sample_menus
):
    sample_menu = sample_menus[0]

    with pytest.raises(
        ValueError,
        match=f"INVALID ARGUMENT: Menu with ID '{sample_menu.id}' already exists.",
    ):
        meal_planning_modification_service.create(sample_menu)


def test_modify_menu_success(
    meal_planning_modification_service, fake_menu_repo, sample_menus
):
    sample_menu = sample_menus[0]
    updated_menu = replace(sample_menu, description="Updated Dinner")
    meal_planning_modification_service.modify(updated_menu)
    saved_menu = fake_menu_repo.get_by_id(sample_menu.id)

    assert saved_menu is not None
    assert saved_menu.description == "Updated Dinner"


def test_modify_menu_not_found_raises_error(meal_planning_modification_service):
    unregistered_menu = Menu(scheduled_date=date(2026, 8, 30), description="Unsaved")

    with pytest.raises(
        ValueError,
        match=f"INVALID ARGUMENT: Menu with ID '{unregistered_menu.id}' does not exist.",
    ):
        meal_planning_modification_service.modify(unregistered_menu)


def test_delete_menu_success(
    meal_planning_modification_service, fake_menu_repo, sample_menus
):
    sample_menu = sample_menus[0]
    meal_planning_modification_service.delete(sample_menu.id)

    assert fake_menu_repo.get_by_id(sample_menu.id) is None


def test_delete_menu_not_found_raises_error(meal_planning_modification_service):
    non_existent_id = uuid4()
    with pytest.raises(
        ValueError,
        match=f"INVALID ARGUMENT: Menu with ID '{non_existent_id}' does not exist.",
    ):
        meal_planning_modification_service.delete(non_existent_id)
