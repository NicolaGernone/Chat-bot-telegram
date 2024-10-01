import logging
import os
from datetime import datetime

from decouple import config

log_dir = "logs"
os.makedirs(log_dir, exist_ok=True)

LOG_FILE = os.path.join(log_dir, f"bot_log_{datetime.now().strftime('%Y-%m-%d')}.log")
LOG_LEVEL = config("LOG_LEVEL", default="INFO").upper()
LOG_FORMAT = "%(asctime)s - %(levelname)s - %(message)s"

logging.basicConfig(filename=LOG_FILE, level=LOG_LEVEL, format=LOG_FORMAT)

# Archivo de logs
file_handler = logging.FileHandler(LOG_FILE)
file_handler.setLevel(LOG_LEVEL)
file_handler.setFormatter(logging.Formatter(LOG_FORMAT))

# Consola
console_handler = logging.StreamHandler()
console_handler.setLevel(LOG_LEVEL)
console_handler.setFormatter(logging.Formatter(LOG_FORMAT))

# Configurar logger
logger = logging.getLogger(__name__)
logger.addHandler(file_handler)
logger.addHandler(console_handler)

FRAMEX_API_URL = config("FRAMEX_API_URL")
TELEGRAM_BOT_TOKEN = config("TELEGRAM_BOT_TOKEN")
