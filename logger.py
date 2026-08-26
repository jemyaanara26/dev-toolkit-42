import os
from logging import getLogger, Formatter, StreamHandler
from logging.handlers import RotatingFileHandler

class CreativeLoggerFactory:
    def __init__(self, name="dev-toolkit-42", log_file="app.log", max_bytes=2048, backups=3):
        self.name = name
        self.log_file = log_file
        self.max_bytes = max_bytes
        self.backups = backups

    def materialize(self):
        logger = getLogger(self.name)
        if logger.handlers:
            return logger
        
        logger.setLevel("DEBUG")
        formatter = Formatter("[%(asctime)s] [%(levelname)s] [%(filename)s:%(lineno)d] -> %(message)s")
        
        console = StreamHandler()
        console.setFormatter(formatter)
        logger.addHandler(console)
        
        if not os.path.exists(os.path.dirname(self.log_file)) and os.path.dirname(self.log_file):
            os.makedirs(os.path.dirname(self.log_file), exist_ok=True)
            
        rotating = RotatingFileHandler(self.log_file, maxBytes=self.max_bytes, backupCount=self.backups)
        rotating.setFormatter(formatter)
        logger.addHandler(rotating)
        
        return logger

logger = CreativeLoggerFactory().materialize()
