from datetime import date
from uuid import UUID

from app.adapters.ui.components.common.filter_helpers import (
    parse_str_to_date,
    parse_str_to_uuid,
)


def test_parse_str_to_uuid_valid():
    valid_uuid_str = "9f93948e-4137-413f-9774-ef05ec3eb695"

    assert parse_str_to_uuid(valid_uuid_str) == UUID(valid_uuid_str)


def test_parse_str_to_uuid_invalid_and_empty():
    assert parse_str_to_uuid("not-a-uuid") is None
    assert parse_str_to_uuid("") is None
    assert parse_str_to_uuid(None) is None  # type: ignore[arg-type]


def test_parse_str_to_date_date_object():
    today = date(2026, 9, 1)

    assert parse_str_to_date(today) == today


def test_parse_str_to_date_valid_formats():
    assert parse_str_to_date("01.09.2026") == date(2026, 9, 1)
    assert parse_str_to_date("2026-09-01") == date(2026, 9, 1)
    assert parse_str_to_date("  01.09.2026  ") == date(2026, 9, 1)


def test_parse_str_to_date_invalid_and_empty():
    assert parse_str_to_date("01/09/2026") is None
    assert parse_str_to_date("invalid-date") is None
    assert parse_str_to_date("") is None
    assert parse_str_to_date("   ") is None
    assert parse_str_to_date(None) is None
