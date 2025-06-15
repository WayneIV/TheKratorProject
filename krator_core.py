"""Central coordinator for the Krator assistant."""

import logging
from typing import Optional

from presence_detector import PresenceDetector
from project_manager import ProjectManager
from voice_interface import VoiceInterface
from context_memory import ContextMemory
from task_router import TaskRouter
from device_bridge import DeviceBridge
from security_layer import SecurityLayer


class KratorCore:
    """Orchestrate all assistant modules and maintain state."""

    def __init__(self) -> None:
        self.logger = logging.getLogger(self.__class__.__name__)
        self.presence = PresenceDetector()
        self.project_manager = ProjectManager()
        self.vision: Optional[object] = None
        self.voice = VoiceInterface()
        self.memory = ContextMemory()
        self.router = TaskRouter(self.project_manager)
        self.devices = DeviceBridge()
        self.security = SecurityLayer()
        self.running = False

    # ------------------------------------------------------------------
    def start(self) -> None:
        """Initialize subsystems and greet the user if present."""
        self.logger.info("Starting KratorCore")
        self.running = True
        if self.presence.is_user_nearby():
            self.voice.speak("Krator online and ready")

    def stop(self) -> None:
        """Cleanly shut down subsystems."""
        self.logger.info("Stopping KratorCore")
        self.running = False
        if self.vision:
            self.vision.close()

    # ------------------------------------------------------------------
    def handle_command(self, text: str) -> None:
        """Route a command string to the task router."""
        text = text.strip()
        if not text:
            return
        self.logger.info("Handling command: %s", text)
        self.memory.add_event("command", text)
        self.router.route_command(text)

    def run_forever(self) -> None:
        """Run the main loop using voice if available, else CLI input."""
        self.start()
        try:
            while self.running:
                if self.voice.recognizer:
                    text = self.voice.listen()
                else:
                    text = input("> ")
                if text.lower() in {"exit", "quit"}:
                    break
                self.handle_command(text)
        finally:
            self.stop()


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    core = KratorCore()
    core.run_forever()
