import asyncio
import datetime
import logging
import sys
import uuid

from aiogram import Bot
from aiogram.client.default import DefaultBotProperties
from aiogram.fsm.storage.redis import RedisStorage
from sqlalchemy import select
from sqlalchemy.dialects.postgresql import insert

import config
from utils.db import AlchemySqlDb
from utils.models_orm import Base
from utils.repositories import ShopRepository

telegram_bot = Bot(token=config.TELEGRAM_BOT_TOKEN, default=DefaultBotProperties(parse_mode=config.TELEGRAM_PARSE_MODE))
redis_storage = RedisStorage.from_url(config.REDIS_URL, state_ttl=config.STATE_TTL, data_ttl=config.DATA_TTL)
logging.basicConfig(level=config.LOG_LEVEL, stream=sys.stdout)

db = AlchemySqlDb(config.SQLALCHEMY_DATABASE_URL, Base)

repo = ShopRepository(db)


async def main():
    print(await repo.db.clean())
    print(await repo.db.prepare())

    # from utils.models_orm import User, Item, Category, OrderItem, Order
    # await db.clean()
    # await db.prepare()
    # async with db.SessionLocal() as session:
    #
    # async with db.SessionLocal() as session:
    #     session.add(Category(name='Goods', text='Товары'))
    #     session.add(Category(name='Services', text='Услуги'))
    #     await session.commit()
    #     category_goods = await session.execute(select(Category).where(Category.name == 'Goods'))
    #     category_goods = category_goods.scalar_one_or_none()
    #     category_services = await session.execute(select(Category).where(Category.name == 'Services'))
    #     category_services = category_services.scalar_one_or_none()
    #     item1 = Item(name='Товар 1', price=100.5, description='Описание товара 1', category=category_goods)
    #     item2 = Item(name='Услуга 1', price=50.5, description='Описание услуги 1', category=category_services)
    #     session.add(item1)
    #     session.add(item2)
    #     await session.commit()
    #     dt = datetime.datetime.utcnow()
    #     user1 = User(firstname='Denis', lastname='Ivanov', username='ivanov_dv', created=dt, updated=dt)
    #     user2 = User(firstname='Denis', lastname='Ivanov', username='ivanov_dv', created=dt, updated=dt)
    #     session.add(user1)
    #     session.add(user2)
    #     await session.commit()
    #     user1 = await session.execute(select(User).where(User.id == 1))
    #     user1 = user1.scalar_one_or_none()
    #     item_order1 = OrderItem(user_id=1, item=item1, quantity=2)
    #     item_order2 = OrderItem(user_id=1, item=item2, quantity=1)
    #     session.add(item_order1)
    #     session.add(item_order2)
    #     await session.commit()
    #     order = Order(
    #         id=uuid.uuid4(),
    #         user_id=1,
    #         order_items=[item_order1, item_order2],
    #         status='created',
    #         created=dt,
    #         updated=dt
    #     )
    #     session.add(order)
    #     await session.commit()
    #     user2 = await session.execute(select(User).where(User.id == 2))
    #     user2 = user2.scalar_one_or_none()
    #     item_order1 = OrderItem(user_id=2, item=item1, quantity=2)
    #     item_order2 = OrderItem(user_id=2, item=item2, quantity=1)
    #     session.add(item_order1)
    #     session.add(item_order2)
    #     await session.commit()
    #     order = Order(
    #         id=uuid.uuid4(),
    #         user_id=2,
    #         order_items=[item_order1, item_order2],
    #         status='created',
    #         created=dt,
    #         updated=dt
    #     )
    #     session.add(order)
    #     await session.commit()
    # async with db.SessionLocal() as session:
    #     user1 = await session.execute(select(User).where(User.id == 1))
    #     user1 = user1.scalar_one_or_none()
    #     print(user1)
    #     item_order1 = OrderItem(user_id=1, item=item1, quantity=2)
    #     item_order2 = OrderItem(user_id=1, item=item2, quantity=1)
    #     session.add(item_order1)
    #     session.add(item_order2)
    #     await session.commit()
    #     items = await session.execute(select(OrderItem).where(OrderItem.user_id == 1, OrderItem.order_id.is_(None)))
    #     items = items.scalars().all()
    #     print(items)
    #     order = Order(
    #         id=uuid.uuid4(),
    #         user_id=1,
    #         order_items=items,
    #         status='created',
    #         created=dt,
    #         updated=dt
    #     )
    #     session.add(order)
    #     await session.commit()


if __name__ == '__main__':
    asyncio.run(main())
