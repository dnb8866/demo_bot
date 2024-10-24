import logging
import os
from datetime import time

from dotenv import load_dotenv

from utils.assist import frange

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
PLANNER
"""
MIN_SLOT_DURATION_MINUTES = 30
START_WORK_DAY_HOUR = 9
END_WORK_DAY_HOUR = 18
PLANNER_SCHEDULE = {
    time(hour=int(time_value), minute=int((time_value - int(time_value)) * 60)): None
    for time_value in frange(START_WORK_DAY_HOUR,
                             END_WORK_DAY_HOUR,
                             1 / (60 / MIN_SLOT_DURATION_MINUTES))
}


"""
REDIS
"""
REDIS_URL = os.getenv('REDIS_URL')
STATE_TTL = 60 * 60 * 24
DATA_TTL = 60 * 60 * 24


"""
POSTGRESQL
"""
POSTGRESQL_USER = os.getenv('POSTGRESQL_USER')
POSTGRESQL_PASSWORD = os.getenv('POSTGRESQL_PASSWORD')
POSTGRESQL_HOST = os.getenv('POSTGRESQL_HOST')
POSTGRESQL_PORT = os.getenv('POSTGRESQL_PORT')
POSTGRESQL_DB = 'demo_bot'
SQLALCHEMY_DB_URL = (f'postgresql+asyncpg://{POSTGRESQL_USER}:{POSTGRESQL_PASSWORD}@{POSTGRESQL_HOST}:'
                           f'{POSTGRESQL_PORT}/{POSTGRESQL_DB}')


"""
POSTGRESQL_TEST
"""
POSTGRESQL_USER = os.getenv('POSTGRESQL_USER_TEST')
POSTGRESQL_PASSWORD = os.getenv('POSTGRESQL_PASSWORD_TEST')
POSTGRESQL_HOST = os.getenv('POSTGRESQL_HOST_TEST')
POSTGRESQL_PORT = os.getenv('POSTGRESQL_PORT_TEST')
POSTGRESQL_DB_TEST = 'demo_bot_test'
SQLALCHEMY_DB_URL_TEST = (f'postgresql+asyncpg://{POSTGRESQL_USER}:{POSTGRESQL_PASSWORD}@{POSTGRESQL_HOST}:'
                                f'{POSTGRESQL_PORT}/{POSTGRESQL_DB_TEST}')
