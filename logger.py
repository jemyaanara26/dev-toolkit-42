import logging
from logging.handlers import RotatingFileHandler, MemoryHandler
import os

def create_rotating_logger(
    name="dev_toolkit",
    log_dir="logs",
    log_file="app.log",
    max_size=5 * 1024 * 1024,
    backup_count=3,
    level=logging.INFO
):
    if not os.path.exists(log_dir):
        os.makedirs(log_dir)
    log_path = os.path.join(log_dir, log_file)
    logger = logging.getLogger(name)
    if logger.handlers:
        return logger
    logger.setLevel(level)
    file_handler = RotatingFileHandler(
        log_path,
        maxBytes=max_size,
        backupCount=backup_count,
        delay=True
    )
    file_formatter = logging.Formatter(
        "%(asctime)s | %(levelname)-8s | %(name)s | %(message)s"
    )
    file_handler.setFormatter(file_formatter)
    logger.addHandler(file_handler)
    console_handler = logging.StreamHandler()
    console_handler.setFormatter(file_formatter)
    logger.addHandler(console_handler)
    mem_handler = MemoryHandler(
        capacity=100,
        flushLevel=logging.ERROR,
        target=file_handler
    )
    logger.addHandler(mem_handler)
    logger.info("Logger initialized with rotation")
    return logger

if __name__ == "__main__":
    logger = create_rotating_logger()
    logger.info("Starting the application")
    for i in range(20):
        logger.debug(f"Debug info {i}")
        if i % 5 == 0:
            logger.warning(f"Warning at step {i}")
        logger.info(f"Processed {i}")
    logger.error("Simulated error to flush memory")
    logger.info("Application finished")