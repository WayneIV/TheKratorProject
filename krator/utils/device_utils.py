"""Utility wrappers for hardware interactions."""

from __future__ import annotations
try:
    import RPi.GPIO as GPIO
except ImportError:  # pragma: no cover - not on all systems
    GPIO = None


def set_pin(pin: int, state: bool) -> None:
    """Set a GPIO pin state."""
    if not GPIO:
        return
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(pin, GPIO.OUT)
    GPIO.output(pin, GPIO.HIGH if state else GPIO.LOW)
