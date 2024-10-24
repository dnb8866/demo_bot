import asyncio

from aiogram import Dispatcher

import config
from engine import telegram_bot, redis_storage, sql_db
from handlers import (
    main_handlers,
    payment_handlers,
    planner_handlers,
    shop_handlers
)


async def main():
    dp = Dispatcher(storage=redis_storage)
    dp.include_routers(
        main_handlers.router,
        payment_handlers.router,
        planner_handlers.router,
        shop_handlers.router
    )
    if sql_db.sql_url == config.SQLALCHEMY_DB_URL_TEST:
        input('Подключена тестовая БД. Нажмите Enter, чтобы продолжить.')
    await sql_db.prepare()
    await dp.start_polling(telegram_bot)
    await telegram_bot.delete_webhook(drop_pending_updates=True)


if __name__ == '__main__':
    asyncio.run(main())
