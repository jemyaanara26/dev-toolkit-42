import logging
from logging.handlers import RotatingFileHandler
import os
from collections import deque

def setup_rotating_logger(name, log_path, max_bytes=1000000, backups=5):
    logger = logging.getLogger(name)
    logger.setLevel(logging.DEBUG)
    log_dir = os.path.dirname(log_path)
    if log_dir and not os.path.exists(log_dir):
        os.makedirs(log_dir)
    handler = RotatingFileHandler(log_path, maxBytes=max_bytes, backupCount=backups)
    handler.setLevel(logging.INFO)
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    handler.setFormatter(formatter)
    logger.addHandler(handler)
    class RecentLogsHandler(logging.Handler):
        def __init__(self, maxlen=10):
            super().__init__()
            self.recent = deque(maxlen=maxlen)
        def emit(self, record):
            self.recent.append(self.format(record))
    recent_handler = RecentLogsHandler()
    recent_handler.setFormatter(formatter)
    logger.addHandler(recent_handler)
    return logger, recent_handler

if __name__ == '__main__':
    logger, recent = setup_rotating_logger('dev-toolkit-42', 'logs/app.log')
    logger.info('Application started with rotating logger')
    logger.debug('This is a debug message')
    logger.warning('Warning message for rotation test')
    print('Recent logs captured:')
    for log in recent.recent:
        print(log)
    print('Logger with rotation is ready.')