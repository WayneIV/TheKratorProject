"""Shared constants for the Krator framework."""

class Colors:
    """ANSI color codes for console output."""

    RESET = "\033[0m"
    RED = "\033[31m"
    GREEN = "\033[32m"
    YELLOW = "\033[33m"
    BLUE = "\033[34m"


class States:
    """Possible core states."""

    INIT = "init"
    RUNNING = "running"
    STOPPED = "stopped"


class Keys:
    """Configuration keys used throughout the project."""

    WAKE_WORD = "krator"
