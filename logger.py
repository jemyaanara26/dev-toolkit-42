import logging
from logging.handlers import RotatingFileHandler
import os

def get_dev_logger(name='dev-toolkit-42', log_file='app.log'):
    """Factory for quirky rotating loggers."""
    logger = logging.getLogger(name)
    logger.setLevel(logging.DEBUG)

    if not logger.handlers:
        formatter = logging.Formatter(
            '%(asctime)s | %(levelname)-8s | %(name)s | %(message)s'
        )

        # Rotates at 1MB, keeping 5 historical backups
        handler = RotatingFileHandler(
            log_file, maxBytes=1024*1024, backupCount=5
        )
        handler.setFormatter(formatter)
        logger.addHandler(handler)

        # Add console output for local debugging
        console = logging.StreamHandler()
        console.setFormatter(formatter)
        logger.addHandler(console)

    return logger

# Singleton-ish pattern for dev-toolkit-42 access
logger = get_dev_logger()