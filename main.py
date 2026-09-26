import logging

import flet as ft

from app.adapters.ui.app import App
from app.infrastructure.container import create_container

logger = logging.getLogger(__name__)


def main() -> None:
    container = create_container()
    app = App(container)
    logger.info("Launched application UI.")
    ft.run(app.__call__, assets_dir=str(container.settings.assets_dir))
    logger.info("Application shut down.")


if __name__ == "__main__":
    main()
