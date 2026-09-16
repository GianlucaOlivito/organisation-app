import logging
from abc import ABC, abstractmethod
from pathlib import Path
from typing import Any
from uuid import UUID

from app.adapters.common.json_file_handler import read_json_file, write_json_file

logger = logging.getLogger(__name__)


class JsonBaseRepository[T](ABC):
    """Generic base repository to manage persistence with JSON."""

    def __init__(self, file_path: Path) -> None:
        self._file_path = file_path
        logger.debug(
            "%s initialized with path: %s",
            self.__class__.__name__,
            self._file_path,
        )

    @abstractmethod
    def _entity_to_dict(self, entity: T) -> dict[str, Any]: ...

    @abstractmethod
    def _dict_to_entity(self, data: dict[str, Any]) -> T: ...

    def get_all(self) -> list[T]:
        raw_data = read_json_file(self._file_path)
        items: list[T] = []
        for item in raw_data:
            try:
                items.append(self._dict_to_entity(item))
            except (KeyError, ValueError, TypeError) as e:
                logger.error("Skipping invalid entity: %s. Error: %s", item, e)
        logger.debug("Retrieved %d entities from %s.", len(items), self._file_path)
        return items

    def get_by_id(self, id: UUID) -> T | None:
        entity = next((item for item in self.get_all() if item.id == id), None)
        if entity:
            logger.debug("Found entity with ID '%s'.", id)
        else:
            logger.debug("No entity found with ID '%s'.", id)
        return entity

    def save(self, entity: T) -> None:
        items = self.get_all()
        updated = False
        for idx, existing in enumerate(items):
            if existing.id == entity.id:
                items[idx] = entity
                updated = True
                break
        if not updated:
            items.append(entity)
        serialized = [self._entity_to_dict(item) for item in items]
        write_json_file(self._file_path, serialized)
        logger.debug("Saved entity (ID: %s) to '%s'.", entity.id, self._file_path)

    def delete(self, id: UUID) -> None:
        items = self.get_all()
        filtered = [item for item in items if item.id != id]
        if len(filtered) != len(items):
            serialized = [self._entity_to_dict(item) for item in filtered]
            write_json_file(self._file_path, serialized)
            logger.debug("Deleted entity with ID '%s' from '%s'.", id, self._file_path)
        else:
            logger.warning("Attempted to delete non-existent entity with ID '%s'.", id)
