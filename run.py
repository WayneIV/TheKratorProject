"""Entry point for launching Krator."""

import logging

from krator.config import settings
from krator.utils.logger import setup_logging
from krator.krator_core import KratorCore


def main() -> None:
    """Configure logging and start the core loop."""
    setup_logging(settings.log_level)
    logging.getLogger(__name__).info("Krator starting")
    core = KratorCore()
    core.run_forever()


if __name__ == "__main__":
    main()
