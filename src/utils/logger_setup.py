from loguru import logger
import sys
from typing import Dict, Any


def setup_logging(config: Dict[str, Any]) -> None:
    """
    Configure logger using the log level from config.
    """
    logger.remove()  # Remove default Loguru handlers to avoid duplicate logs
    level = config.get("logging", {}).get("level", "INFO")
    logger.add(sys.stderr, level=level)  # Log to standard error with configured level
    logger.info(f"Logging initialized at level: {level}")
