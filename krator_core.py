"""Central coordinator for the Krator assistant."""

from typing import Optional

from presence_detector import PresenceDetector
from project_manager import ProjectManager
from vision_module import VisionModule
from voice_interface import VoiceInterface
from task_router import TaskRouter
from device_bridge import DeviceBridge
from security_layer import SecurityLayer


class KratorCore:
    """Skeleton orchestrator that wires together all assistant modules."""

    def __init__(self):
        self.presence = PresenceDetector()
        self.project_manager = ProjectManager()
        self.vision: Optional[VisionModule] = None
        self.voice = VoiceInterface()
        self.router = TaskRouter(self.project_manager)
        self.devices = DeviceBridge()
        self.security = SecurityLayer()

    def start(self):
        """Placeholder start method for initializing modules."""
        if self.presence.is_user_nearby():
            self.voice.speak("Krator online and ready")
        # Additional startup logic would be implemented here.

    def handle_command(self, text: str):
        """Route a command string to the task router."""
        self.router.route_command(text)
