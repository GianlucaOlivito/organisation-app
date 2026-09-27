import math
from dataclasses import FrozenInstanceError
from uuid import UUID, uuid4

import pytest

from app.domain.meal_planning.course import Course


def test_create_valid_course():
    recipe_id = uuid4()
    course = Course(recipe_id=recipe_id, portions=2)

    assert course.recipe_id == recipe_id
    assert course.portions == 2


def test_create_course_converts_valid_string_inputs():
    raw_uuid = str(uuid4())
    course = Course(recipe_id=raw_uuid, portions="3,0")

    assert isinstance(course.recipe_id, UUID)
    assert course.recipe_id == UUID(raw_uuid)
    assert course.portions == 3


@pytest.mark.parametrize("invalid_portions", [0, -10, -1.5, "0", "-5"])
def test_course_raises_error_for_non_positive_portions(invalid_portions):
    with pytest.raises(ValueError, match="Ungültige Anzahl Portionen"):
        Course(recipe_id=uuid4(), portions=invalid_portions)


@pytest.mark.parametrize(
    "invalid_portions",
    [
        "invalid",
        "2.5",
        2.5,
        math.nan,
        math.inf,
        -math.inf,
        None,
        [],
    ],
)
def test_course_raises_error_for_invalid_portions_format(invalid_portions):
    with pytest.raises(ValueError, match="Ungültige Anzahl Portionen"):
        Course(recipe_id=uuid4(), portions=invalid_portions)  # type: ignore[arg-type]


@pytest.mark.parametrize("invalid_id", [None, "not-a-uuid", 123, "", "   "])
def test_course_raises_error_for_invalid_recipe_id(invalid_id):
    with pytest.raises(ValueError, match="Ungültige Rezept-ID"):
        Course(recipe_id=invalid_id, portions=1)  # type: ignore[arg-type]


def test_course_is_immutable():
    course = Course(recipe_id=uuid4(), portions=2)

    with pytest.raises(FrozenInstanceError):
        course.portions = 5  # type: ignore[misc]
