import logging
import os

from dotenv import load_dotenv


dotenv_path = os.path.join(os.path.dirname(__file__), '.env')
if os.path.exists(dotenv_path):
    load_dotenv(dotenv_path)


'''
LOGGING LEVEL
'''
LOG_LEVEL = logging.INFO


'''
Telegram API
'''
TELEGRAM_BOT_TOKEN = os.getenv('TELEGRAM_BOT_TOKEN')
TELEGRAM_PARSE_MODE = 'HTML'
MAX_SESSION_TIME_SECS = 300


"""
Payments
"""
SBER_TOKEN = os.getenv('SBER_TOKEN')
YOOKASSA_TOKEN = os.getenv('YOOKASSA_TOKEN')
PAYMASTER_TOKEN = os.getenv('PAYMASTER_TOKEN')


"""
REDIS
"""
REDIS_URL = os.getenv('REDIS_URL')
STATE_TTL = 60 * 60 * 24
DATA_TTL = 60 * 60 * 24


"""
POSTGRESQL
"""
POSTGRESQL_USER = os.getenv("POSTGRESQL_USER")
POSTGRESQL_PASSWORD = os.getenv("POSTGRESQL_PASSWORD")
POSTGRESQL_HOST = os.getenv("POSTGRESQL_HOST")
POSTGRESQL_PORT = os.getenv("POSTGRESQL_PORT")
POSTGRESQL_DB = "demo_bot"
SQLALCHEMY_DATABASE_URL = (f"postgresql+asyncpg://{POSTGRESQL_USER}:{POSTGRESQL_PASSWORD}@{POSTGRESQL_HOST}:"
                           f"{POSTGRESQL_PORT}/{POSTGRESQL_DB}")


"""
POSTGRESQL_TEST
"""
POSTGRESQL_USER = os.getenv("POSTGRESQL_USER_TEST")
POSTGRESQL_PASSWORD = os.getenv("POSTGRESQL_PASSWORD_TEST")
POSTGRESQL_HOST = os.getenv("POSTGRESQL_HOST_TEST")
POSTGRESQL_PORT = os.getenv("POSTGRESQL_PORT_TEST")
POSTGRESQL_DB = "demo_bot_test"
SQLALCHEMY_DATABASE_URL_TEST = (f"postgresql+asyncpg://{POSTGRESQL_USER}:{POSTGRESQL_PASSWORD}@{POSTGRESQL_HOST}:"
                                f"{POSTGRESQL_PORT}/{POSTGRESQL_DB}")