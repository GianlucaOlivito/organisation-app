import logging

from app.infrastructure.logging_setup import setup_logging

logger = logging.getLogger(__name__)


def main():
    setup_logging()
    logger.info("Application initialized.")


if __name__ == "__main__":
    main()
