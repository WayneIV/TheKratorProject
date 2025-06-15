from __future__ import annotations
import os
from dataclasses import dataclass


def _get_env(key: str, default: str | None = None) -> str | None:
    """Return environment variable value or default."""
    return os.getenv(key, default)


@dataclass
class Settings:
    """Runtime configuration loaded from environment variables."""

    log_level: str = _get_env("KRATOR_LOG_LEVEL", "INFO")
    data_dir: str = _get_env("KRATOR_DATA_DIR", "data")
    device_id: str | None = _get_env("KRATOR_DEVICE_ID")


settings = Settings()
