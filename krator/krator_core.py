"""Multithreaded Flask-based API core for the Krator assistant."""

from __future__ import annotations
import base64
import logging
import os
import threading
import time
from typing import Any, Dict, Optional

from flask import Flask, jsonify, request
import cv2

# Import modules from top-level package wrappers
from modules.voice_interface import VoiceInterface
from modules.vision_module import VisionModule
from modules.context_memory import ContextMemory
from modules.project_manager import ProjectManager

LOG_PATH = os.path.join("data", "logs", "krator.log")
os.makedirs(os.path.dirname(LOG_PATH), exist_ok=True)
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
    handlers=[logging.FileHandler(LOG_PATH), logging.StreamHandler()],
)


class KratorCore:
    """Core coordinator exposing a Flask API and running module threads."""

    def __init__(self) -> None:
        self.logger = logging.getLogger(self.__class__.__name__)
        self.voice = VoiceInterface()
        try:
            self.vision: Optional[VisionModule] = VisionModule()
        except Exception as exc:  # pragma: no cover - hardware dependent
            self.logger.warning("Vision module unavailable: %s", exc)
            self.vision = None
        self.memory = ContextMemory()
        self.projects = ProjectManager()
        self.running = False
        self.threads: list[threading.Thread] = []

        self.app = Flask(__name__)
        self._register_routes()

    # ------------------------------------------------------------------
    def _register_routes(self) -> None:
        """Configure Flask route handlers."""

        @self.app.post("/voice/input")
        def voice_input() -> Any:
            """Process a text command via the voice interface."""
            data = request.get_json(silent=True) or {}
            text = str(data.get("text", ""))
            try:
                response = self.voice.process_command(text)
                return jsonify({"response": response})
            except Exception as exc:  # pragma: no cover - runtime protection
                self.logger.exception("Voice processing failed")
                return jsonify({"error": str(exc)}), 500

        @self.app.get("/vision/snapshot")
        def vision_snapshot() -> Any:
            """Return a base64 encoded snapshot from the vision module."""
            if not self.vision:
                return jsonify({"error": "vision unavailable"}), 503
            frame = self.vision.get_current_frame()
            if frame is None:
                return jsonify({"error": "no frame"}), 500
            ret, buf = cv2.imencode(".jpg", frame)
            if not ret:
                return jsonify({"error": "encoding failed"}), 500
            b64 = base64.b64encode(buf.tobytes()).decode("ascii")
            return jsonify({"image": b64})

        @self.app.get("/memory/context")
        def memory_context() -> Any:
            """Return recent context memory."""
            return jsonify(self.memory.get_recent_context())

        @self.app.post("/project/task")
        def project_task() -> Any:
            """Add or update a task via the project manager."""
            data = request.get_json(silent=True) or {}
            try:
                self.projects.add_or_update_task(data)
                return jsonify({"status": "ok"})
            except Exception as exc:  # pragma: no cover - runtime protection
                self.logger.exception("Project manager error")
                return jsonify({"error": str(exc)}), 500

        @self.app.get("/status/modules")
        def status_modules() -> Any:
            """Report operational status of all modules."""
            status: Dict[str, Any] = {
                "voice": self.voice.recognizer is not None,
                "vision": bool(self.vision and self.vision.capture),
                "memory": True,
                "projects": True,
            }
            return jsonify(status)

    # ------------------------------------------------------------------
    def _start_threads(self) -> None:
        """Spawn daemon threads for long-running modules."""
        self.logger.info("Starting module threads")
        loops = [
            threading.Thread(target=self._voice_loop, daemon=True),
            threading.Thread(target=self._vision_loop, daemon=True),
            threading.Thread(target=self._memory_loop, daemon=True),
            threading.Thread(target=self._project_loop, daemon=True),
        ]
        for thread in loops:
            thread.start()
            self.threads.append(thread)

    # ------------------------------------------------------------------
    def _voice_loop(self) -> None:
        """Continuously listen for voice commands."""
        while self.running:
            if not self.voice.recognizer:
                time.sleep(1)
                continue
            try:
                text = self.voice.listen()
                if text:
                    self.memory.add_event("voice", text)
                    self.voice.process_command(text)
            except Exception as exc:  # pragma: no cover - runtime protection
                self.logger.error("Voice loop error: %s", exc)

    def _vision_loop(self) -> None:
        """Capture frames for context when the camera is available."""
        if not self.vision:
            return
        while self.running:
            try:
                frame = self.vision.read_frame()
                if frame is not None:
                    self.memory.add_event("vision", "frame")
                else:
                    time.sleep(0.5)
            except Exception as exc:  # pragma: no cover - runtime protection
                self.logger.error("Vision loop error: %s", exc)
                break

    def _memory_loop(self) -> None:
        """Periodic housekeeping for memory management."""
        while self.running:
            time.sleep(60)

    def _project_loop(self) -> None:
        """Placeholder project manager loop."""
        while self.running:
            time.sleep(60)

    # ------------------------------------------------------------------
    def start(self, host: str = "0.0.0.0", port: int = 8000) -> None:
        """Start all threads and run the Flask server."""
        self.logger.info("KratorCore starting")
        self.running = True
        self._start_threads()
        self.app.run(host=host, port=port, threaded=True)

    def stop(self) -> None:
        """Signal all threads to stop."""
        self.logger.info("KratorCore stopping")
        self.running = False
        if self.vision:
            self.vision.close()


if __name__ == "__main__":
    core = KratorCore()
    core.start()
