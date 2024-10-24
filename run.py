import asyncio

from aiogram import Dispatcher

import config
from engine import telegram_bot, redis_storage, shop_repo, db
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
    if db.sql_url == config.SQLALCHEMY_DB_URL_TEST:
        input('Подключена тестовая БД. Нажмите Enter, чтобы продолжить.')
    await shop_repo.db.prepare()
    await dp.start_polling(telegram_bot)
    await telegram_bot.delete_webhook(drop_pending_updates=True)


if __name__ == '__main__':
    asyncio.run(main())
