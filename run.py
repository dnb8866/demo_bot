import asyncio

from aiogram import Dispatcher

from engine import telegram_bot, redis_storage
from handlers import main_handlers, payment_handlers, shop_handlers


async def main():
    dp = Dispatcher(storage=redis_storage)
    dp.include_routers(
        main_handlers.router,
        payment_handlers.router,
        shop_handlers.router
    )
    await dp.start_polling(telegram_bot)
    await telegram_bot.delete_webhook(drop_pending_updates=True)


if __name__ == '__main__':
    asyncio.run(main())
