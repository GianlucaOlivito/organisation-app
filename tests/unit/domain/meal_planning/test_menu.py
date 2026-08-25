from datetime import UTC, datetime
from uuid import UUID, uuid4

from app.domain.meal_planning.course import Course
from app.domain.meal_planning.menu import Menu


def test_create_menu_with_defaults() -> None:
    today = datetime.now(UTC).date()
    menu = Menu(description="lunch", scheduled_date=today)

    assert isinstance(menu.id, UUID)
    assert menu.description == "lunch"
    assert menu.scheduled_date == today
    assert menu.courses == []


def test_create_menu_with_custom_attributes() -> None:
    course = Course(recipe_id=uuid4(), portions=3)
    today = datetime.now(UTC).date()
    menu = Menu(description="dinner", scheduled_date=today, courses=[course])

    assert menu.description == "dinner"
    assert len(menu.courses) == 1
    assert menu.courses[0] == course


def test_menu_instances_have_unique_uuids_and_isolated_lists() -> None:
    today = datetime.now(UTC).date()
    menu_1 = Menu(description="Menu 1", scheduled_date=today)
    menu_2 = Menu(description="Menu 2", scheduled_date=today)

    assert menu_1.id != menu_2.id

    course = Course(recipe_id=uuid4(), portions=1)
    menu_1.courses.append(course)

    assert len(menu_1.courses) == 1
    assert len(menu_2.courses) == 0
