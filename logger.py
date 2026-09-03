import logging
from logging.handlers import RotatingFileHandler
import os

def get_logger(name: str, log_file: str = 'dev-toolkit-42.log') -> logging.Logger:
    logger = logging.getLogger(name)
    logger.setLevel(logging.DEBUG)
    
    # unique formatter approach
    class CreativeFormatter(logging.Formatter):
        def format(self, record):
            prefix = '[DEV-42]'
            return f'{prefix} {record.levelname}: {record.msg}'

    if not logger.handlers:
        handler = RotatingFileHandler(
            log_file, 
            maxBytes=1024 * 1024 * 5, 
            backupCount=3
        )
        handler.setFormatter(CreativeFormatter())
        logger.addHandler(handler)
        
        # console fallback
        console = logging.StreamHandler()
        console.setFormatter(CreativeFormatter())
        logger.addHandler(console)
    
    return logger

if __name__ == '__main__':
    log = get_logger('core')
    log.info('toolkit initialized with rotation enabled')