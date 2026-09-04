from dataclasses import FrozenInstanceError
from uuid import uuid4

import pytest

from app.domain.meal_planning.course import Course


def test_create_valid_course():
    recipe_id = uuid4()
    course = Course(recipe_id=recipe_id, portions=2)

    assert course.recipe_id == recipe_id
    assert course.portions == 2


@pytest.mark.parametrize("invalid_portions", [0, -10])
def test_course_raises_error_for_non_positive_portions(invalid_portions):
    with pytest.raises(
        ValueError, match="INVALID ARGUMENT: Course portions must be positive."
    ):
        Course(recipe_id=uuid4(), portions=invalid_portions)


@pytest.mark.parametrize("invalid_id", [None, "not-a-uuid", 123])
def test_course_raises_error_for_invalid_recipe_id(invalid_id):
    with pytest.raises(
        ValueError, match="INVALID ARGUMENT: Course must refer to a valid recipe."
    ):
        Course(recipe_id=invalid_id, portions=1)  # type: ignore[arg-type]


def test_course_is_immutable():
    course = Course(recipe_id=uuid4(), portions=2)

    with pytest.raises(FrozenInstanceError):
        course.portions = 5  # type: ignore[misc]
