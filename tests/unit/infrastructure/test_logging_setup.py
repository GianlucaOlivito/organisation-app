import logging
from unittest.mock import patch

from app.infrastructure.logging_setup import (
    AppFilter,
    CustomLogFormatter,
    MemoryLogHandler,
    setup_logging,
)


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


def test_custom_log_formatter_applies_ansi_codes():
    formatter = CustomLogFormatter("%(levelname)s | %(message)s", use_colors=True)
    record = logging.LogRecord(
        "app", logging.INFO, "path", 10, "Test log message", (), None
    )
    formatted_output = formatter.format(record)

    assert CustomLogFormatter.COLORS["INFO"] in formatted_output
    assert CustomLogFormatter.COLORS["RESET"] in formatted_output
    assert "INFO | Test log message" in formatted_output


def test_custom_log_formatter_injects_location():
    formatter = CustomLogFormatter("%(location)s | %(message)s")
    record = logging.LogRecord(
        "app", logging.INFO, "path", 10, "Test location", (), None
    )
    record.module = "test_module"
    record.lineno = 42
    formatted_output = formatter.format(record)

    assert record.location == "test_module:42"
    assert "test_module:42 | Test location" in formatted_output


def test_memory_log_handler_appends_formatted_message(log_buffer):
    handler = MemoryLogHandler(log_buffer)
    handler.setFormatter(logging.Formatter("%(levelname)s: %(message)s"))
    record = logging.LogRecord("app", logging.INFO, "path", 10, "Buffer test", (), None)
    handler.emit(record)
    snapshot = log_buffer.take_snapshot()

    assert len(snapshot) == 1
    assert snapshot[0] == ("INFO", "INFO: Buffer test")


def test_memory_log_handler_handles_exceptions_gracefully(log_buffer):
    handler = MemoryLogHandler(log_buffer)
    record = logging.LogRecord("app", logging.INFO, "path", 10, "Error test", (), None)
    with (
        patch.object(handler, "format", side_effect=Exception("Format error")),
        patch.object(handler, "handleError") as mock_handle_error,
    ):
        handler.emit(record)
        mock_handle_error.assert_called_once_with(record)


def test_setup_logging_configures_handlers_and_creates_directory(
    clean_root_logger, log_buffer, tmp_path
):
    mock_log_file = tmp_path / "logs" / "test.log"
    with patch("app.infrastructure.logging_setup.settings") as mock_settings:
        mock_settings.log_level = "DEBUG"
        mock_settings.log_file_path = mock_log_file
        setup_logging(log_buffer)

        assert clean_root_logger.level == logging.DEBUG

        app_handlers = [
            h
            for h in clean_root_logger.handlers
            if "LogCaptureHandler" not in h.__class__.__name__
        ]

        assert len(app_handlers) == 3
        assert mock_log_file.parent.exists()


def test_setup_logging_is_idempotent(clean_root_logger, log_buffer, tmp_path):
    mock_log_file = tmp_path / "logs" / "test.log"
    with patch("app.infrastructure.logging_setup.settings") as mock_settings:
        mock_settings.log_level = "INFO"
        mock_settings.log_file_path = mock_log_file
        setup_logging(log_buffer)
        initial_count = len(clean_root_logger.handlers)
        setup_logging(log_buffer)

        assert len(clean_root_logger.handlers) == initial_count
