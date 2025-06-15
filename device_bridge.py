"""Lightweight bridge for sending commands between devices."""

from __future__ import annotations

import logging
from collections import defaultdict
from typing import DefaultDict, List


class DeviceBridge:
    """In-memory queue based communication layer."""

    def __init__(self) -> None:
        self.logger = logging.getLogger(self.__class__.__name__)
        self._queues: DefaultDict[str, List[str]] = defaultdict(list)

    def send_command(self, device_id: str, command: str) -> None:
        """Transmit a command to another device."""
        self.logger.info("Sending '%s' to %s", command, device_id)
        self._queues[device_id].append(command)

    def fetch_commands(self, device_id: str) -> List[str]:
        """Retrieve and clear queued commands for a device."""
        commands = self._queues.pop(device_id, [])
        return commands
