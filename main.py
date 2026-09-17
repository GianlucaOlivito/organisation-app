import logging

import flet as ft

from app.adapters.ui.app import App
from app.infrastructure.container import create_container
from app.infrastructure.logging_setup import setup_logging

logger = logging.getLogger(__name__)


def main() -> None:
    setup_logging()
    logger.info("Starting application...")
    app = App(create_container())
    ft.run(app.__call__)
    logger.info("Application closed.")


if __name__ == "__main__":
    main()
