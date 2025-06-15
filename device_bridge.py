"""Lightweight bridge for sending commands between devices."""


class DeviceBridge:
    """Placeholder for MQTT/WebSocket based communication layer."""

    def __init__(self):
        # Setup networking clients or message queues
        pass

    def send_command(self, device_id: str, command: str) -> None:
        """Transmit a command to another device."""
        # TODO: implement real messaging between devices
        print(f"Sending '{command}' to {device_id}")
