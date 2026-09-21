import json
import logging
from pathlib import Path
from typing import Any

logger = logging.getLogger(__name__)


def read_json_file(file_path: Path) -> list[dict[str, Any]]:
    if not file_path.exists():
        return []
    try:
        with open(file_path, mode="r", encoding="utf-8") as f:
            data = json.load(f)
            return data if isinstance(data, list) else []
    except json.JSONDecodeError as e:
        logger.error(
            "Failed to decode '%s': %s. Returned empty list.", file_path.name, e
        )
        return []
    except OSError as e:
        logger.error(
            "Failed to access '%s': %s. Returned empty list.", file_path.name, e
        )
        return []


def write_json_file(file_path: Path, data: list[dict[str, Any]]) -> None:
    try:
        file_path.parent.mkdir(parents=True, exist_ok=True)
        with open(file_path, mode="w", encoding="utf-8") as f:
            json.dump(data, f, indent=4, ensure_ascii=False)
    except OSError as e:
        logger.error("Failed to write '%s': %s", file_path.name, e)
        raise
