"""GPIO control for Raspberry Pi."""

try:
    import RPi.GPIO as GPIO
except ImportError:  # pragma: no cover - not on Raspberry Pi
    GPIO = None


class GPIOController:
    def __init__(self):
        if GPIO:
            GPIO.setmode(GPIO.BCM)
        self.available = GPIO is not None

    def setup_output(self, pin: int):
        if self.available:
            GPIO.setup(pin, GPIO.OUT)

    def set_high(self, pin: int):
        if self.available:
            GPIO.output(pin, GPIO.HIGH)

    def set_low(self, pin: int):
        if self.available:
            GPIO.output(pin, GPIO.LOW)

    def cleanup(self):
        if self.available:
            GPIO.cleanup()
