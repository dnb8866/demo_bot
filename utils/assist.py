from decimal import Decimal

from aiogram import types, Bot


async def calculate_total_price_from_items(order_items: list):
    total = Decimal('0')
    for item in order_items:
        total += Decimal(str(item.item.price)) * item.quantity
    return total


async def delete_prev_messages(bot: Bot, message: types.Message, prev_msg_id: int):
    await bot.delete_message(message.chat.id, prev_msg_id)
    await message.delete()


def frange(start, end, step):
    res = start
    while res < end:
        yield res
        res += step
