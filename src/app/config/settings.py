from dataclasses import dataclass
from pathlib import Path

ROOT_DIR: Path = next(
    p for p in Path(__file__).resolve().parents if (p / "pyproject.toml").exists()
)


@dataclass(frozen=True, slots=True)
class Settings:
    """Utility class for application settings."""

    app_title: str = "Savoria"
    assets_dir: Path = ROOT_DIR / "assets"
    app_logo_file_name: str = "logo.ico"
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
