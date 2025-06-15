"""Detect user presence using network and sensor checks."""

import logging
import subprocess
from typing import Iterable, List


class PresenceDetector:
    """Lightweight detector for user or device proximity."""

    def __init__(self, known_wifi: Iterable[str] | None = None, known_bt: Iterable[str] | None = None):
        self.logger = logging.getLogger(self.__class__.__name__)
        self.known_wifi = set(m.lower() for m in (known_wifi or []))
        self.known_bt = set(a.lower() for a in (known_bt or []))

    # ------------------------------------------------------------------
    def is_user_nearby(self) -> bool:
        """Return True if any known device is detected."""
        wifi = self._detect_wifi()
        bt = self._detect_bluetooth()
        nearby = bool(wifi or bt)
        self.logger.debug("WiFi devices detected: %s", wifi)
        self.logger.debug("Bluetooth devices detected: %s", bt)
        return nearby

    # WiFi detection ----------------------------------------------------
    def _detect_wifi(self) -> List[str]:
        found: List[str] = []
        if not self.known_wifi:
            return found
        try:
            output = subprocess.check_output(["arp", "-a"], text=True)
        except Exception as exc:  # pragma: no cover - platform dependent
            self.logger.warning("ARP scan failed: %s", exc)
            return found
        for line in output.splitlines():
            parts = line.split()
            if len(parts) >= 4:
                mac = parts[3].lower()
                if mac in self.known_wifi:
                    found.append(mac)
        return found

    # Bluetooth detection ----------------------------------------------
    def _detect_bluetooth(self) -> List[str]:
        found: List[str] = []
        if not self.known_bt:
            return found
        try:
            output = subprocess.check_output(["bluetoothctl", "devices"], text=True)
        except Exception as exc:  # pragma: no cover - platform dependent
            self.logger.warning("Bluetooth scan failed: %s", exc)
            return found
        for line in output.splitlines():
            parts = line.strip().split()
            if len(parts) >= 2:
                addr = parts[1].lower()
                if addr in self.known_bt:
                    found.append(addr)
        return found


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    detector = PresenceDetector()
    print("User nearby?", detector.is_user_nearby())
