from __future__ import annotations

from collections import defaultdict
from dataclasses import dataclass
from datetime import UTC, datetime
from typing import Any, Callable


def _now_iso() -> str:
    return datetime.now(UTC).replace(microsecond=0).isoformat()


@dataclass
class JarvisEvent:
    type: str
    payload: dict[str, Any]
    created_at: str


class EventBus:
    def __init__(self) -> None:
        self._handlers: dict[str, list[Callable[[JarvisEvent], None]]] = defaultdict(list)

    def subscribe(self, event_type: str, handler: Callable[[JarvisEvent], None]) -> None:
        self._handlers[event_type].append(handler)

    def emit(self, event_type: str, payload: dict[str, Any]) -> JarvisEvent:
        event = JarvisEvent(type=event_type, payload=payload, created_at=_now_iso())
        for handler in self._handlers.get(event_type, []):
            handler(event)
        for handler in self._handlers.get('*', []):
            handler(event)
        return event
