from dataclasses import dataclass
from pathlib import Path

ROOT_DIR: Path = next(
    p for p in Path(__file__).resolve().parents if (p / "pyproject.toml").exists()
)


@dataclass(frozen=True, slots=True)
class Settings:
    """Utility class for application settings."""

    log_level: str = "INFO"
    log_file_path: Path = ROOT_DIR / "logs" / "app.log"
    recipes_file_path: Path = ROOT_DIR / "data" / "recipes.json"
    menus_file_path: Path = ROOT_DIR / "data" / "menus.json"
    inventory_file_path: Path = ROOT_DIR / "data" / "inventory.json"


settings = Settings()
