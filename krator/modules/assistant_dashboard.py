"""Web dashboard for Krator."""

from __future__ import annotations
import threading
from fastapi import FastAPI
import uvicorn


class AssistantDashboard:
    """Launch a lightweight web dashboard."""

    def __init__(self, host: str = "0.0.0.0", port: int = 8000) -> None:
        self.app = FastAPI()
        self.host = host
        self.port = port

        @self.app.get("/")
        def read_root():
            return {"status": "ok"}

    def start(self) -> None:
        """Run the web server in a background thread."""
        thread = threading.Thread(target=self._run, daemon=True)
        thread.start()

    def _run(self) -> None:
        uvicorn.run(self.app, host=self.host, port=self.port, log_level="warning")
