import sys
from dataclasses import dataclass
from pathlib import Path

if getattr(sys, "frozen", False):
    ROOT_DIR = Path(sys.executable).parent
else:
    ROOT_DIR: Path = next(
        p for p in Path(__file__).resolve().parents if (p / "pyproject.toml").exists()
    )


@dataclass(frozen=True, slots=True)
class Settings:
    """Utility class for application settings."""

    app_title: str = "Savoria"
    app_version: str = "1.0.0"
    assets_dir: Path = ROOT_DIR / "assets"
    app_logo_ico: str = "logo.ico"
    app_logo_png: str = "logo.png"
    window_width: int = 1000
    window_height: int = 700
    window_min_width: int = 800
    window_min_height: int = 550
    log_level: str = "DEBUG"
    log_file_path: Path = ROOT_DIR / "logs" / "app.log"
    log_buffer_size: int = 1000
    recipes_file_path: Path = ROOT_DIR / "data" / "recipes.json"
    menus_file_path: Path = ROOT_DIR / "data" / "menus.json"
    inventory_file_path: Path = ROOT_DIR / "data" / "inventory.json"
    shopping_list_file_path: Path = ROOT_DIR / "exports" / "shopping_list.md"


settings = Settings()
