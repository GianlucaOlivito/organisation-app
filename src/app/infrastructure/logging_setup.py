import logging
from logging.handlers import TimedRotatingFileHandler
from typing import ClassVar

from app.config.settings import settings
from app.infrastructure.log_buffer import LogBuffer


class MemoryLogHandler(logging.Handler):
    """Represents custom log handler to buffer logs in memory for UI presentation."""

    def __init__(self, buffer: LogBuffer) -> None:
        super().__init__()
        self._buffer = buffer

    def emit(self, record: logging.LogRecord) -> None:
        try:
            self._buffer.append(record.levelname, self.format(record))
        except Exception:  # noqa: BLE001
            self.handleError(record)


class AppFilter(logging.Filter):
    """Filters log records, allowing only those originating from app."""

    def filter(self, record: logging.LogRecord) -> bool:
        return record.name.startswith(("app", "__main__"))


class CustomLogFormatter(logging.Formatter):
    """Formats log records with combined location and optional ANSI colors."""

    COLORS: ClassVar[dict[str, str]] = {
        "DEBUG": "\033[38;5;152m",  # light blue
        "INFO": "\033[38;5;114m",  # green
        "WARNING": "\033[38;5;214m",  # orange
        "ERROR": "\033[38;5;168m",  # red
        "CRITICAL": "\033[37;48;5;168m",  # white on red background
        "RESET": "\033[0m",
    }

    def __init__(self, fmt: str | None = None, *, use_colors: bool = False) -> None:
        super().__init__(fmt)
        self.use_colors = use_colors

    def format(self, record: logging.LogRecord) -> str:
        record.location = f"{record.module}:{record.lineno}"
        log_message = super().format(record)
        if not self.use_colors:
            return log_message
        color_code = self.COLORS.get(record.levelname, self.COLORS["RESET"])
        return f"{color_code}{log_message}{self.COLORS['RESET']}"


def setup_logging(buffer: LogBuffer) -> None:
    FORMAT = "%(asctime)s | %(levelname)-8s | %(location)-36s | %(message)s"
    logger = logging.getLogger()
    logger.setLevel(settings.log_level)
    if any(isinstance(h, MemoryLogHandler) for h in logger.handlers):
        return
    settings.log_file_path.parent.mkdir(parents=True, exist_ok=True)
    plain_formatter = CustomLogFormatter(FORMAT, use_colors=False)
    app_filter = AppFilter()
    file_handler = TimedRotatingFileHandler(
        filename=settings.log_file_path,
        when="H",
        interval=1,
        backupCount=168,
        encoding="utf-8",
    )
    file_handler.suffix = "%Y-%m-%d_%H-%M-%S"
    file_handler.setFormatter(plain_formatter)
    console_handler = logging.StreamHandler()
    console_handler.setFormatter(CustomLogFormatter(FORMAT, use_colors=True))
    memory_handler = MemoryLogHandler(buffer)
    memory_handler.setFormatter(plain_formatter)
    for handler in (file_handler, console_handler, memory_handler):
        handler.addFilter(app_filter)
        logger.addHandler(handler)
