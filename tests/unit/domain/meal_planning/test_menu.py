from datetime import UTC, date, datetime
from uuid import UUID, uuid4

import pytest

from app.domain.meal_planning.course import Course
from app.domain.meal_planning.menu import Menu


def test_create_valid_menu():
    course = Course(recipe_id=uuid4(), portions=3)
    today = datetime.now(UTC).date()
    menu = Menu(description="  dinner  ", scheduled_date=today, courses=[course])

    assert menu.description == "dinner"
    assert menu.scheduled_date == today
    assert len(menu.courses) == 1
    assert menu.courses[0] == course


def test_create_menu_with_iso_date_string():
    course = Course(recipe_id=uuid4(), portions=1)
    menu = Menu(
        description="Lunch",
        scheduled_date="2026-09-27",
        courses=[course],
    )

    assert isinstance(menu.scheduled_date, date)
    assert menu.scheduled_date == date(2026, 9, 27)


@pytest.mark.parametrize("invalid_desc", ["", "   ", None])
def test_menu_raises_error_for_invalid_description(invalid_desc):
    course = Course(recipe_id=uuid4(), portions=1)

    with pytest.raises(ValueError, match="Ungültige Menübeschreibung"):
        Menu(
            description=invalid_desc,  # type: ignore[arg-type]
            scheduled_date=datetime.now(UTC).date(),
            courses=[course],
        )


@pytest.mark.parametrize("invalid_date", ["2026-13-45", "not-a-date", 12345, None])
def test_menu_raises_error_for_invalid_date(invalid_date):
    course = Course(recipe_id=uuid4(), portions=1)

    with pytest.raises(TypeError, match="Ungültiges Datum"):
        Menu(
            description="Dinner",
            scheduled_date=invalid_date,  # type: ignore[arg-type]
            courses=[course],
        )


def test_menu_raises_error_for_empty_courses():
    with pytest.raises(ValueError, match="Ungültige Gangliste"):
        Menu(
            description="Dinner",
            scheduled_date=datetime.now(UTC).date(),
            courses=[],
        )


def test_menu_instances_have_unique_uuids_and_isolated_lists():
    today = datetime.now(UTC).date()
    course1 = Course(recipe_id=uuid4(), portions=1)
    course2 = Course(recipe_id=uuid4(), portions=1)
    menu_1 = Menu(description="Menu 1", scheduled_date=today, courses=[course1])
    menu_2 = Menu(description="Menu 2", scheduled_date=today, courses=[course2])

    assert isinstance(menu_1.id, UUID)
    assert menu_1.id != menu_2.id

    extra_course = Course(recipe_id=uuid4(), portions=1)
    menu_1.courses.append(extra_course)

    assert len(menu_1.courses) == 2
    assert len(menu_2.courses) == 1
