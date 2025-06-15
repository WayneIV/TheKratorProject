"""Manage tasks and projects with a lightweight JSON backend."""

from __future__ import annotations

import json
import os
from datetime import date, datetime
from typing import Dict, List


class ProjectManager:
    """Very small scale task tracker used by the assistant."""

    def __init__(self, db_path: str = "tasks.json") -> None:
        self.db_path = db_path
        if not os.path.exists(self.db_path):
            with open(self.db_path, "w", encoding="utf-8") as fh:
                json.dump({}, fh)

    # ------------------------------------------------------------------
    def _load(self) -> Dict[str, List[dict]]:
        with open(self.db_path, "r", encoding="utf-8") as fh:
            return json.load(fh)

    def _save(self, data: Dict[str, List[dict]]) -> None:
        with open(self.db_path, "w", encoding="utf-8") as fh:
            json.dump(data, fh, indent=2)

    # ------------------------------------------------------------------
    def get_overdue_tasks(self, project: str) -> List[str]:
        """Return a list of overdue task descriptions for the given project."""
        data = self._load().get(project, [])
        overdue: List[str] = []
        today = date.today()
        for task in data:
            due = task.get("due")
            completed = task.get("completed", False)
            if not completed and due:
                try:
                    if datetime.fromisoformat(due).date() < today:
                        overdue.append(task.get("notes", ""))
                except ValueError:
                    continue
        return overdue

    def update_task(self, task_id: str, notes: str) -> None:
        """Update a task with new notes or create it if missing."""
        data = self._load()
        for project, tasks in data.items():
            for task in tasks:
                if task.get("id") == task_id:
                    task["notes"] = notes
                    self._save(data)
                    return
        # If not found, add as a new task under "general"
        data.setdefault("general", []).append({"id": task_id, "notes": notes})
        self._save(data)

    def add_or_update_task(self, task: dict) -> None:
        """Create or update a task using provided data."""
        tid = task.get("id") or str(int(datetime.utcnow().timestamp()))
        notes = task.get("notes", "")
        project = task.get("project", "general")
        data = self._load()
        tasks = data.setdefault(project, [])
        for existing in tasks:
            if existing.get("id") == tid:
                existing.update(task)
                self._save(data)
                return
        new_task = {"id": tid, "notes": notes}
        if "due" in task:
            new_task["due"] = task["due"]
        tasks.append(new_task)
        self._save(data)
