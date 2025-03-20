import logging
import os

LOG_DIR = os.path.join(os.path.dirname(__file__), "data")
LOG_FILE = os.path.join(LOG_DIR, "logs.txt")

# Ensure the log directory exists
os.makedirs(LOG_DIR, exist_ok=True)

# Create logger
logger = logging.getLogger("app_logger")
logger.setLevel(logging.INFO)

# Create file handler
file_handler = logging.FileHandler(LOG_FILE)
file_handler.setLevel(logging.INFO)

# Create console handler (stdout)
console_handler = logging.StreamHandler()
console_handler.setLevel(logging.INFO)

# Create log format
formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")
file_handler.setFormatter(formatter)
console_handler.setFormatter(formatter)

# Add handlers to the logger
logger.addHandler(file_handler)
logger.addHandler(console_handler)