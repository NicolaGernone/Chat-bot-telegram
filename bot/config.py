from decouple import config

LOG_LEVEL = config('LOG_LEVEL', default='INFO').upper()
LOG_FORMAT = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'

logging.basicConfig(
    level=LOG_LEVEL,
    format=LOG_FORMAT
)

logger = logging.getLogger(__name__)

FRAMEX_API_URL = config('FRAMEX_API_URL')
TELEGRAM_BOT_TOKEN = config('TELEGRAM_BOT_TOKEN')
