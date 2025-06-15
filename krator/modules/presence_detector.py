"""Detect user presence via Wi-Fi or Bluetooth devices."""

from __future__ import annotations
import logging
import subprocess
from typing import Iterable, List


class PresenceDetector:
    """Simple device presence detection."""

    def __init__(self, known_wifi: Iterable[str] | None = None, known_bt: Iterable[str] | None = None) -> None:
        self.logger = logging.getLogger(self.__class__.__name__)
        self.known_wifi = {m.lower() for m in (known_wifi or [])}
        self.known_bt = {a.lower() for a in (known_bt or [])}

    def is_user_nearby(self) -> bool:
        """Return True if a known device is in range."""
        wifi = self._detect_wifi()
        bt = self._detect_bluetooth()
        if wifi:
            self.logger.debug("Known Wi-Fi device detected: %s", wifi)
        if bt:
            self.logger.debug("Known Bluetooth device detected: %s", bt)
        return bool(wifi or bt)

    # ------------------------------------------------------------------
    def _detect_wifi(self) -> List[str]:
        found: List[str] = []
        if not self.known_wifi:
            return found
        try:
            output = subprocess.check_output(["arp", "-a"], text=True)
        except Exception as exc:  # pragma: no cover - system dependent
            self.logger.warning("ARP scan failed: %s", exc)
            return found
        for line in output.splitlines():
            parts = line.split()
            if len(parts) >= 4:
                mac = parts[3].lower()
                if mac in self.known_wifi:
                    found.append(mac)
        return found

    # ------------------------------------------------------------------
    def _detect_bluetooth(self) -> List[str]:
        found: List[str] = []
        if not self.known_bt:
            return found
        try:
            output = subprocess.check_output(["bluetoothctl", "devices"], text=True)
        except Exception as exc:  # pragma: no cover - system dependent
            self.logger.warning("Bluetooth scan failed: %s", exc)
            return found
        for line in output.splitlines():
            parts = line.strip().split()
            if len(parts) >= 2:
                addr = parts[1].lower()
                if addr in self.known_bt:
                    found.append(addr)
        return found
