#import the requirements
import logging
import os
from logging.handlers import RotatingFileHandler

LOG_FILE = "trading.log"
MAX_BYTES = 5 * 1024 * 1024  #rotate after 5MB
BACKUP_COUNT = 3 #keep last 3 log files

#function definition with type hints parameter -> name: str, return type -> logger.Logger
def get_logger(name: str) -> logging.Logger:
    # Create (or retrieve) a logger object with the given name
    logger = logging.getLogger(name)

    # If the logger already has handlers attached, return it directly
    # This prevents adding duplicate handlers when the function is called multiple times
    if logger.handlers:
        return logger

    # Set the logger’s level to DEBUG so it captures all messages (DEBUG and above)
    logger.setLevel(logging.DEBUG)

    # Define a formatter: controls how log messages look (timestamp, level, name, message)
    formatter = logging.Formatter(
        fmt="%(asctime)s | %(levelname)-8s | %(name)s | %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S"
    )

    # Create a file handler that writes logs to a file
    # RotatingFileHandler automatically rotates the log file when it reaches MAX_BYTES
    # and keeps BACKUP_COUNT number of old log files
    file_handler = RotatingFileHandler(LOG_FILE, maxBytes=MAX_BYTES, backupCount=BACKUP_COUNT)
    file_handler.setLevel(logging.DEBUG)        # Capture all levels in the file
    file_handler.setFormatter(formatter)        # Apply the formatter to file logs

    # Create a console handler that outputs logs to the terminal
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.WARNING)   # Only show WARNING and above in console
    console_handler.setFormatter(formatter)     # Apply the same formatter

    # Attach both handlers to the logger
    logger.addHandler(file_handler)
    logger.addHandler(console_handler)

    # Return the configured logger object
    return logger
