"""Context memory storage for Krator assistant."""

import json
import logging
import os
from collections import deque
from typing import Deque, Dict, List

from event_logger import EventLogger


class ContextMemory:
    """Provide short-term and long-term memory persistence."""

    def __init__(self, short_term_limit: int = 50, db_path: str = "memory.db", json_path: str = "long_term.json"):
        self.logger = logging.getLogger(self.__class__.__name__)
        self.short_term: Deque[Dict[str, str]] = deque(maxlen=short_term_limit)
        self.events = EventLogger(db_path)
        self.json_path = json_path
        if not os.path.exists(self.json_path):
            with open(self.json_path, "w", encoding="utf-8") as f:
                json.dump({}, f)

    # Short-term memory -----------------------------------------------------
    def add_event(self, event_type: str, data: str) -> None:
        """Add an event to short-term memory and persist to database."""
        self.logger.debug("Adding event %s: %s", event_type, data)
        item = {"type": event_type, "data": data}
        self.short_term.append(item)
        self.events.log_event(event_type, data)

    def recent_events(self, limit: int = 10) -> List[Dict[str, str]]:
        """Return the most recent events from short-term memory."""
        return list(self.short_term)[-limit:]

    def get_recent_context(self) -> List[Dict[str, str]]:
        """Alias for ``recent_events`` for API convenience."""
        return self.recent_events()

    # Long-term memory ------------------------------------------------------
    def remember(self, key: str, value: str) -> None:
        """Persist a key/value pair for long-term recall."""
        self.logger.debug("Storing long-term memory %s", key)
        data = self._load_long_term()
        data[key] = value
        self._save_long_term(data)

    def recall(self, key: str) -> str:
        """Retrieve a value from long-term memory or empty string."""
        data = self._load_long_term()
        return data.get(key, "")

    # Helper methods --------------------------------------------------------
    def _load_long_term(self) -> Dict[str, str]:
        with open(self.json_path, "r", encoding="utf-8") as f:
            return json.load(f)

    def _save_long_term(self, data: Dict[str, str]) -> None:
        with open(self.json_path, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    mem = ContextMemory()
    mem.add_event("test", "module started")
    mem.remember("greeting", "Hello Wayne")
    print("Recent:", mem.recent_events())
    print("Recall:", mem.recall("greeting"))
