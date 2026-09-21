from collections import deque
from collections.abc import Callable


class LogBuffer:
    """Represents a custom buffer for UI presentation of logs."""

    def __init__(self, maxlen: int) -> None:
        self._entries = deque(maxlen=maxlen)
        self._listeners = set()

    def append(self, level: str, message: str) -> None:
        self._entries.append((level, message))
        for listener in tuple(self._listeners):
            listener()

    def take_snapshot(self) -> list[tuple[str, str]]:
        return list(self._entries)

    def clear(self) -> None:
        self._entries.clear()
        for listener in tuple(self._listeners):
            listener()

    def subscribe(self, listener: Callable[[], None]) -> None:
        self._listeners.add(listener)

    def unsubscribe(self, listener: Callable[[], None]) -> None:
        self._listeners.discard(listener)
