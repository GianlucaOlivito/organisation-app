import logging
from logging.handlers import TimedRotatingFileHandler
from typing import ClassVar

from app.config.settings import settings


class AppFilter(logging.Filter):
    """Filters log records, allowing only those originating from app."""

    def filter(self, record: logging.LogRecord) -> bool:
        return record.name.startswith(("app", "__main__"))


class ColoredFormatter(logging.Formatter):
    """Applies ANSI colors to log records based on log level."""

    COLORS: ClassVar[dict[str, str]] = {
        "DEBUG": "\033[38;5;152m",  # light blue
        "INFO": "\033[38;5;114m",  # green
        "WARNING": "\033[38;5;214m",  # orange
        "ERROR": "\033[38;5;168m",  # red
        "CRITICAL": "\033[37;48;5;168m\033[1m",  # white on red background, bold
        "RESET": "\033[0m",
    }

    def format(self, record: logging.LogRecord) -> str:
        color_code = self.COLORS.get(record.levelname, self.COLORS["RESET"])
        log_message = super().format(record)
        return f"{color_code}{log_message}{self.COLORS['RESET']}"


def setup_logging() -> None:
    FORMAT = "%(asctime)s | %(levelname)-8s | %(module)-10s:%(lineno)-3d | %(message)s"
    logger = logging.getLogger()
    logger.setLevel(settings.log_level)
    if any(
        isinstance(getattr(h, "formatter", None), ColoredFormatter)
        for h in logger.handlers
    ):
        return
    settings.log_file_path.parent.mkdir(parents=True, exist_ok=True)
    file_handler = TimedRotatingFileHandler(
        filename=settings.log_file_path,
        when="H",
        interval=1,
        backupCount=168,
        encoding="utf-8",
    )
    file_handler.suffix = "%Y-%m-%d_%H-%M-%S"
    file_handler.setFormatter(logging.Formatter(FORMAT))
    file_handler.addFilter(AppFilter())
    console_handler = logging.StreamHandler()
    console_handler.setFormatter(ColoredFormatter(FORMAT))
    logger.addHandler(file_handler)
    logger.addHandler(console_handler)
