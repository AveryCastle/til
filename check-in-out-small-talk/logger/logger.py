import os
import logging
from logging.handlers import TimedRotatingFileHandler

# Constants
LOG_DIR = "blackhole/log"

# Setup logging
os.makedirs(LOG_DIR, exist_ok=True)
log_file_path = os.path.join(LOG_DIR, "app.log")
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)
handler = TimedRotatingFileHandler(
    log_file_path,
    when="midnight",
    interval=1,
    backupCount=7
)
handler.suffix = "%Y-%m-%d"
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)
if logger.hasHandlers():
    logger.handlers.clear()
logger.addHandler(handler)
