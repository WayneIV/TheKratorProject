"""Route parsed commands to the appropriate subsystem."""

from project_manager import ProjectManager


class TaskRouter:
    """Very small command router placeholder."""

    def __init__(self, manager: ProjectManager):
        self.manager = manager

    def route_command(self, command: str) -> None:
        """Send a text command to the relevant handler."""
        if command.lower().startswith("show overdue"):
            # Example parsing logic
            project = command.partition("from ")[2]
            tasks = self.manager.get_overdue_tasks(project)
            print(tasks)
        # More natural language commands would be handled here
