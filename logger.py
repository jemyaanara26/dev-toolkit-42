import logging
from logging.handlers import RotatingFileHandler
import os
from pathlib import Path
def setup_logger(name="dev-toolkit-42", log_path="logs/app.log", max_size=10485760, backups=3, log_level=logging.INFO):
    logger = logging.getLogger(name)
    logger.setLevel(log_level)
    while logger.handlers:
        logger.removeHandler(logger.handlers[0])
    log_file = Path(log_path)
    log_file.parent.mkdir(parents=True, exist_ok=True)
    file_handler = RotatingFileHandler(
        filename=str(log_file),
        maxBytes=max_size,
        backupCount=backups,
        encoding="utf-8",
        delay=True
    )
    formatter = logging.Formatter(
        "%(asctime)s [%(levelname)s] %(name)s: %(message)s",
        datefmt="%d-%m-%Y %H:%M:%S"
    )
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)
    if os.getenv("ENV", "dev") != "prod":
        stream_handler = logging.StreamHandler()
        stream_handler.setFormatter(formatter)
        logger.addHandler(stream_handler)
    return logger

logger = setup_logger()