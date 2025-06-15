"""Main task engine and module router."""

from __future__ import annotations
import logging
from typing import Optional

from .modules.presence_detector import PresenceDetector
from .modules.project_manager import ProjectManager
from .modules.voice_interface import VoiceInterface
from .modules.context_memory import ContextMemory
from .modules.device_bridge import DeviceBridge
from .modules.security_layer import SecurityLayer
from .modules.automation_engine import AutomationEngine
from .modules.vision_module import VisionModule


class KratorCore:
    """Central orchestrator for Krator."""

    def __init__(self) -> None:
        self.logger = logging.getLogger(self.__class__.__name__)
        self.presence = PresenceDetector()
        self.project_manager = ProjectManager()
        self.voice = VoiceInterface()
        self.memory = ContextMemory()
        self.devices = DeviceBridge()
        self.security = SecurityLayer()
        self.automation = AutomationEngine()
        self.vision: Optional[VisionModule] = None
        self.running = False

    def start(self) -> None:
        """Initialize modules and greet the user."""
        self.logger.info("Starting KratorCore")
        self.running = True
        if self.presence.is_user_nearby():
            self.voice.speak("Krator online and ready")

    def stop(self) -> None:
        """Shutdown modules."""
        self.logger.info("Stopping KratorCore")
        self.running = False
        if self.vision:
            self.vision.close()

    def handle_command(self, text: str) -> None:
        """Basic command handler."""
        text = text.strip()
        if not text:
            return
        self.logger.info("Handling command: %s", text)
        self.memory.add_event("command", text)
        if text.lower() == "status":
            self.voice.speak("System nominal")
        elif text.lower().startswith("send "):
            _, device_id, command = text.split(maxsplit=2)
            self.devices.send_command(device_id, command)

    def run_forever(self) -> None:
        """Run a simple command loop."""
        self.start()
        try:
            while self.running:
                text = self.voice.listen() if self.voice.recognizer else input("> ")
                if text.lower() in {"quit", "exit"}:
                    break
                self.handle_command(text)
        finally:
            self.stop()
