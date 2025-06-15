"""System diagnostics utilities."""

from __future__ import annotations
import os
import psutil


def cpu_usage() -> float:
    """Return CPU usage percentage."""
    return psutil.cpu_percent(interval=0.1)


def memory_usage() -> float:
    """Return memory usage percentage."""
    mem = psutil.virtual_memory()
    return mem.percent
