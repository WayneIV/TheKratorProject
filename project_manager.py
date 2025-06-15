"""Manage tasks and projects across third-party services."""

from typing import List


class ProjectManager:
    """Skeleton interface for task management tools."""

    def __init__(self):
        # Placeholder for API client configuration
        pass

    def get_overdue_tasks(self, project: str) -> List[str]:
        """Return a list of overdue task descriptions for the given project."""
        # TODO: integrate Notion, Google Workspace or Trello
        return []

    def update_task(self, task_id: str, notes: str) -> None:
        """Update a task with new notes or status."""
        # TODO: implement update logic via the chosen API
        pass
