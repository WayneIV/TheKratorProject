"""Rule-based automation engine."""

from __future__ import annotations
import logging
from typing import Callable, Dict


class AutomationEngine:
    """Execute actions based on simple conditional rules."""

    def __init__(self) -> None:
        self.logger = logging.getLogger(self.__class__.__name__)
        self.rules: Dict[str, Callable[[], None]] = {}

    def add_rule(self, trigger: str, action: Callable[[], None]) -> None:
        """Register a trigger-action pair."""
        self.rules[trigger] = action

    def execute(self, trigger: str) -> None:
        """Execute the action for a trigger if it exists."""
        action = self.rules.get(trigger)
        if action:
            self.logger.info("Executing automation trigger: %s", trigger)
            action()
