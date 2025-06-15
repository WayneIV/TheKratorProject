"""Short-term and long-term memory for Krator."""

from __future__ import annotations
import logging
from collections import deque
from typing import Deque, Tuple


class ContextMemory:
    """Simple in-memory store for recent events."""

    def __init__(self, max_events: int = 100) -> None:
        self.logger = logging.getLogger(self.__class__.__name__)
        self.events: Deque[Tuple[str, str]] = deque(maxlen=max_events)

    def add_event(self, kind: str, data: str) -> None:
        """Record an event in memory."""
        self.logger.debug("Storing event %s: %s", kind, data)
        self.events.append((kind, data))

    def recall(self) -> list[Tuple[str, str]]:
        """Return all stored events."""
        return list(self.events)
