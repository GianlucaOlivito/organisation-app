from datetime import date

import pytest

from app.application.common.validators import validate_date_range


def test_validate_date_range_valid_period_succeeds():
    validate_date_range(date(2026, 1, 1), date(2026, 1, 10))


def test_validate_date_range_same_day_succeeds():
    validate_date_range(date(2026, 1, 1), date(2026, 1, 1))


def test_validate_date_range_start_after_end_raises_value_error():
    with pytest.raises(
        ValueError, match="INVALID ARGUMENT: Start date cannot be after end date."
    ):
        validate_date_range(date(2026, 1, 10), date(2026, 1, 1))
