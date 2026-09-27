import logging
from collections.abc import Generator

import pytest

from app.infrastructure.log_buffer import LogBuffer


@pytest.fixture
def log_buffer() -> LogBuffer:
    return LogBuffer(maxlen=1000)


@pytest.fixture
def clean_root_logger() -> Generator[logging.Logger]:
    logger = logging.getLogger()
    original_handlers = logger.handlers[:]
    logger.handlers.clear()
    yield logger
    for handler in logger.handlers:
        handler.close()
    logger.handlers = original_handlers
