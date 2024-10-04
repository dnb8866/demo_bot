import asyncio
import logging
import sys

from aiogram import Bot
from aiogram.client.default import DefaultBotProperties
from aiogram.fsm.storage.redis import RedisStorage
from sqlalchemy import select

import config
from utils.db import AlchemySqlDb
from utils.models_orm import Base
from utils.repositories import ShopRepository, UserRepository, PlannerRepository

telegram_bot = Bot(token=config.TELEGRAM_BOT_TOKEN, default=DefaultBotProperties(parse_mode=config.TELEGRAM_PARSE_MODE))
redis_storage = RedisStorage.from_url(config.REDIS_URL, state_ttl=config.STATE_TTL, data_ttl=config.DATA_TTL)
logging.basicConfig(level=config.LOG_LEVEL, stream=sys.stdout)

db = AlchemySqlDb(config.SQLALCHEMY_SHOP_DB_URL, Base)

user_repo = UserRepository(db)
shop_repo = ShopRepository(db)
planner_repo = PlannerRepository(db)


# async def main():
#
#     from utils.models_orm import User, Item, Category, OrderItem, Order, Slot, Event, AvailableDate
#     import datetime as dt
#
#     dt_1 = dt.datetime.utcnow()

    # user_1 = User(firstname='Denis', created=dt_1, updated=dt_1)
    #
    # event_1 = Event(name='event_1', duration=90, description='event_1')
    # event_2 = Event(name='event_2', duration=120, description='event_2')
    # event_3 = Event(name='event_3', duration=45, description='event_2')
    #
    # date_1 = AvailableDate(event_date=dt.date(2024, 1, 1))
    # date_2 = AvailableDate(event_date=dt.date(2024, 1, 2))
    #
    # slot_1 = Slot(event=event_1, start_date=date_1, start_time=dt.time(10), user=user_1, status=SlotStatus.PENDING, created=dt_1, updated=dt_1)
    # slot_2 = Slot(event=event_2, start_date=date_1, start_time=dt.time(13), user=user_1, status=SlotStatus.PENDING, created=dt_1, updated=dt_1)
    # slot_3 = Slot(event=event_3, start_date=date_1, start_time=dt.time(17), user=user_1, status=SlotStatus.PENDING, created=dt_1, updated=dt_1)
    # slot_4 = Slot(event=event_1, start_date=date_2, start_time=dt.time(12), user=user_1, status=SlotStatus.PENDING, created=dt_1, updated=dt_1)

    # async with db.SessionLocal() as session:
        # session.add(date_1)
        # session.add(date_2)
        # session.add(event_1)
        # session.add(event_2)
        # session.add(event_3)
        # session.add(slot_1)
        # session.add(slot_2)
        # session.add(slot_3)
        # session.add(slot_4)
        # await session.commit()

        # slot_orm = (await session.execute(
        #     select(Slot).where(Slot.id == 4)
        # )).unique().scalar_one_or_none()
        # print(slot_orm.status)
        #
        # day_orm = (await session.execute(
        #     select(AvailableDate).where(AvailableDate.event_date == dt.date(2024, 1, 3))
        # )).unique().scalar_one_or_none()
        # print(day_orm.slots)

    # event = Event(name='Стрижка', description='Описание', duration=60)
    # event = await planner_repo.add_event(event)
    # dt = datetime.datetime.utcnow()
    # slot = Slot(
    #     user_id=123,
    #     event_id=event.id,
    #     start_date=datetime.date(2024, 9, 21),
    #     start_time=datetime.time(18),
    #     status=SlotStatus.PENDING,
    #     created=dt,
    #     updated=dt
    # )
    # slot = await planner_repo.add_slot(slot)
    # print(slot)
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
