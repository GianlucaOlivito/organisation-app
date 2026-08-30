from datetime import date
from uuid import uuid4

import pytest

from app.application.meal_planning.modification_service import MenuModificationService
from app.domain.meal_planning.menu import Menu


@pytest.fixture
def modification_service(fake_menu_repo) -> MenuModificationService:
    return MenuModificationService(menu_repository=fake_menu_repo)


@pytest.fixture
def sample_menu() -> Menu:
    return Menu(
        id=uuid4(), scheduled_date=date(2026, 8, 30), description="Lunch", courses=[]
    )


def test_create_menu_success(modification_service, fake_menu_repo, sample_menu):
    created_menu = modification_service.create(sample_menu)

    assert created_menu == sample_menu
    assert fake_menu_repo.get_by_id(sample_menu.id) == sample_menu


def test_create_menu_already_exists_raises_error(
    modification_service, fake_menu_repo, sample_menu
):
    fake_menu_repo.save(sample_menu)

    with pytest.raises(
        ValueError,
        match=f"INVALID ARGUMENT: Menu with ID '{sample_menu.id}' already exists.",
    ):
        modification_service.create(sample_menu)


def test_modify_menu_success(modification_service, fake_menu_repo, sample_menu):
    fake_menu_repo.save(sample_menu)
    updated_menu = Menu(
        id=sample_menu.id,
        scheduled_date=sample_menu.scheduled_date,
        description="Updated Dinner",
        courses=[],
    )
    modification_service.modify(updated_menu)
    saved_menu = fake_menu_repo.get_by_id(sample_menu.id)

    assert saved_menu is not None
    assert saved_menu.description == "Updated Dinner"


def test_modify_menu_not_found_raises_error(modification_service, sample_menu):
    with pytest.raises(
        ValueError,
        match=f"INVALID ARGUMENT: Menu with ID '{sample_menu.id}' does not exist.",
    ):
        modification_service.modify(sample_menu)


def test_delete_menu_success(modification_service, fake_menu_repo, sample_menu):
    fake_menu_repo.save(sample_menu)
    modification_service.delete(sample_menu.id)

    assert fake_menu_repo.get_by_id(sample_menu.id) is None


def test_delete_menu_not_found_raises_error(modification_service):
    non_existent_id = uuid4()
    with pytest.raises(
        ValueError,
        match=f"INVALID ARGUMENT: Menu with ID '{non_existent_id}' does not exist.",
    ):
        modification_service.delete(non_existent_id)
