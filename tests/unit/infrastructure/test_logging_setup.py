import logging
from unittest.mock import patch

import pytest

from app.infrastructure.logging_setup import AppFilter, ColoredFormatter, setup_logging


@pytest.fixture
def clean_root_logger():
    """Resets root logger handlers before and after test execution."""

    logger = logging.getLogger()
    original_handlers = logger.handlers[:]
    logger.handlers.clear()
    yield logger
    for handler in logger.handlers:
        handler.close()
    logger.handlers = original_handlers


def test_app_filter_accepts_allowed_namespaces():
    app_filter = AppFilter()
    app_record = logging.LogRecord(
        "app.service", logging.INFO, "path", 10, "msg", (), None
    )
    main_record = logging.LogRecord(
        "__main__", logging.INFO, "path", 10, "msg", (), None
    )

    assert app_filter.filter(app_record) is True
    assert app_filter.filter(main_record) is True


def test_app_filter_rejects_external_namespaces():
    app_filter = AppFilter()
    third_party_record = logging.LogRecord(
        "urllib3.connectionpool", logging.INFO, "path", 10, "msg", (), None
    )

    assert app_filter.filter(third_party_record) is False


def test_colored_formatter_applies_ansi_codes():
    formatter = ColoredFormatter("%(levelname)s | %(message)s")
    record = logging.LogRecord(
        "app", logging.INFO, "path", 10, "Test log message", (), None
    )

    formatted_output = formatter.format(record)

    assert ColoredFormatter.COLORS["INFO"] in formatted_output
    assert ColoredFormatter.COLORS["RESET"] in formatted_output
    assert "INFO | Test log message" in formatted_output


def test_setup_logging_configures_handlers_and_creates_directory(
    clean_root_logger, tmp_path
):
    mock_log_file = tmp_path / "logs" / "test.log"

    with patch("app.infrastructure.logging_setup.settings") as mock_settings:
        mock_settings.log_level = "DEBUG"
        mock_settings.log_file_path = mock_log_file
        setup_logging()

        assert clean_root_logger.level == logging.DEBUG
        app_handlers = [
            h
            for h in clean_root_logger.handlers
            if "LogCaptureHandler" not in h.__class__.__name__
        ]
        assert len(app_handlers) == 2
        assert mock_log_file.parent.exists()


def test_setup_logging_is_idempotent(clean_root_logger, tmp_path):
    mock_log_file = tmp_path / "logs" / "test.log"

    with patch("app.infrastructure.logging_setup.settings") as mock_settings:
        mock_settings.log_level = "INFO"
        mock_settings.log_file_path = mock_log_file
        setup_logging()
        initial_count = len(clean_root_logger.handlers)
        setup_logging()

        assert len(clean_root_logger.handlers) == initial_count
