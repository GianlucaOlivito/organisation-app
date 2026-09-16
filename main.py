import logging

from app.infrastructure.container import create_container
from app.infrastructure.logging_setup import setup_logging

logger = logging.getLogger(__name__)


def main() -> None:
    setup_logging()
    create_container()
    logger.info("Application initialized.")


if __name__ == "__main__":
    main()
