from decouple import config
import logging

log_dir = "logs"
os.makedirs(log_dir, exist_ok=True)

LOG_FILE = os.path.join(log_dir, f"bot_log_{datetime.now().strftime('%Y-%m-%d')}.log")
LOG_LEVEL = config("LOG_LEVEL", default="INFO").upper()
LOG_FORMAT = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"

logging.basicConfig(filename=LOG_FILE, level=LOG_LEVEL, format=LOG_FORMAT)

logger = logging.getLogger(__name__)

FRAMEX_API_URL = config("FRAMEX_API_URL")
TELEGRAM_BOT_TOKEN = config("TELEGRAM_BOT_TOKEN")
