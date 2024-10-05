import datetime

from sqlalchemy import select, delete, update, extract

from utils.db import AlchemySqlDb
from utils.exceptions import OrderItemsNotFound, OrderItemNotFound
from utils.models_orm import OrderItem, Order, User, Category, Item, Event, Slot, AvailableDate


class UserRepository:
    def __init__(self, db: AlchemySqlDb):
        self.db = db

    async def add(self, user: User) -> User:
        async with self.db.SessionLocal() as session:
            session.add(user)
            await session.commit()
            return user

    async def get(self, user_id: int) -> User | None:
        async with self.db.SessionLocal() as session:
            return (await session.execute(select(User).where(User.id == user_id))).scalar_one_or_none()

    async def update(self, user: User) -> User:
        async with self.db.SessionLocal() as session:
            user.updated = datetime.datetime.utcnow()
            await session.execute(
                update(User)
                .values(
                    firstname=user.firstname,
                    lastname=user.lastname,
                    username=user.username,
                    ban=user.ban,
                    updated=user.updated,
                )
                .where(User.id == user.id)
            )
            await session.commit()
            return user

    async def delete(self, user_id: int) -> None:
        async with self.db.SessionLocal() as session:
            await session.execute(delete(User).where(User.id == user_id))
            await session.commit()


class ShopRepository:
    def __init__(self, db: AlchemySqlDb):
        self.db = db

    async def add_order_item(self, user_id: int, item_id: int, quantity: int) -> OrderItem:
        async with self.db.SessionLocal() as session:
            dt_now = datetime.datetime.utcnow()
            order_item = OrderItem(user_id=user_id, item_id=item_id, quantity=quantity, created=dt_now, updated=dt_now)
            session.add(order_item)
            await session.commit()
            return order_item

    async def get_order_item(self, order_item_id: int, without_order=False) -> OrderItem | None:
        async with self.db.SessionLocal() as session:
            order_item = (await session.execute(
                select(OrderItem).where(OrderItem.id == order_item_id)
            )).scalar_one_or_none()
            return order_item

    async def get_all_order_items(self, user_id: int, without_order=False) -> list[OrderItem]:
        async with self.db.SessionLocal() as session:
            if without_order:
                return (await session.execute(
                    select(OrderItem).where(OrderItem.user_id == user_id, OrderItem.order_id.is_(None)))
                        ).scalars().all()
            return (await session.execute(select(OrderItem).where(OrderItem.user_id == user_id))).scalars().all()


    async def update_order_item(self, order_item_id: int, quantity: int) -> OrderItem:
        async with self.db.SessionLocal() as session:
            order_item = (await session.execute(
                select(OrderItem).where(OrderItem.id == order_item_id)
            )).scalar_one_or_none()
            if not order_item:
                raise OrderItemNotFound
            order_item.quantity = quantity
            await session.commit()
            return order_item

    async def delete_order_item(self, order_item_id: int) -> None:
        async with self.db.SessionLocal() as session:
            await session.execute(
                delete(OrderItem).where(OrderItem.id == order_item_id)
            )
            await session.commit()

    async def create_order(self, user_id: int, items: list[OrderItem]) -> Order:
        async with self.db.SessionLocal() as session:
            dt = datetime.datetime.utcnow()
            order = Order(
                user_id=user_id,
                order_items=items,
                status='created',
                created=dt,
                updated=dt
            )
            session.add(order)
            await session.commit()
            return order

    async def get_order(self, order_id: str) -> Order | None:
        async with self.db.SessionLocal() as session:
            order = await session.execute(select(Order).where(Order.id == order_id))
            return order.unique().scalar_one_or_none()

    async def get_all_orders_from_user(self, user_id: int) -> list[Order] | None:
        async with self.db.SessionLocal() as session:
            return (await session.execute(select(Order).where(Order.user_id == user_id))).unique().scalars().all()

    async def change_order_status(self, order_id: int, new_status: str) -> Order:
        async with self.db.SessionLocal() as session:
            order = await session.execute(select(Order).where(Order.id == order_id))
            order = order.unique().scalar_one_or_none()
            order.status = new_status
            order.updated = datetime.datetime.utcnow()
            await session.commit()
            return order

    async def delete_order(self, order_id: str) -> None:
        async with self.db.SessionLocal() as session:
            await session.execute(delete(Order).where(Order.id == order_id))
            await session.commit()

    async def get_categories(self) -> list[tuple[int, str]]:
        async with self.db.SessionLocal() as session:
            return (await session.execute(select(Category.id, Category.text))).all()

    async def get_items_by_category(self, category_id: int) -> list[tuple[int, str]]:
        async with self.db.SessionLocal() as session:
            return (await session.execute(select(Item.id, Item.name).where(Item.category_id == category_id))).all()

    async def get_item(self, item_id: int) -> Item | None:
        async with self.db.SessionLocal() as session:
            return (await session.execute(select(Item).where(Item.id == item_id))).scalar_one_or_none()


class PlannerRepository:
    def __init__(self, db: AlchemySqlDb):
        self.db = db

    async def add_event(self, event: Event) -> Event:
        async with self.db.SessionLocal() as session:
            session.add(event)
            await session.commit()
            return event

    async def get_event(self, event_id: int):
        async with self.db.SessionLocal() as session:
            return (await session.execute(select(Event).where(Event.id == event_id))).scalar_one_or_none()

    async def update_event(self, event: Event) -> Event:
        async with self.db.SessionLocal() as session:
            event.updated = datetime.datetime.utcnow()
            await session.execute(
                update(Event)
                .values(
                    name=event.name,
                    description=event.description,
                    duration=event.duration,
                    updated=event.updated,
                )
                .where(Event.id == event.id)
            )
            await session.commit()
            return event

    async def delete_event(self, event_id: int) -> None:
        async with self.db.SessionLocal() as session:
            await session.execute(delete(Event).where(Event.id == event_id))
            await session.commit()

    async def add_slot(self, slot: Slot) -> Slot:
        async with self.db.SessionLocal() as session:
            session.add(slot)
            await session.commit()
            return slot

    async def get_slot(self, slot_id: int) -> Slot | None:
        async with self.db.SessionLocal() as session:
            return (await session.execute(select(Slot).where(Slot.id == slot_id))).scalar_one_or_none()

    async def get_slots_for_user(self, user_id: int) -> list[Slot] | None:
        async with self.db.SessionLocal() as session:
            return (await session.execute(select(Slot).where(Slot.user_id == user_id))).scalars().all()

    async def update_slot(self, slot: Slot) -> Slot:
        async with self.db.SessionLocal() as session:
            slot.updated = datetime.datetime.utcnow()
            await session.execute(
                update(Slot)
                .values(
                    user_id=slot.user_id,
                    event_id=slot.event_id,
                    start_date_id=slot.start_date_id,
                    start_time=slot.start_time,
                    status=slot.status,
                    updated=slot.updated,
                )
                .where(Slot.id == slot.id)
            )
            await session.commit()
            return slot

    async def delete_slot(self, slot_id: int) -> None:
        async with self.db.SessionLocal() as session:
            await session.execute(delete(Slot).where(Slot.id == slot_id))
            await session.commit()

    async def add_available_date(self, available_date: AvailableDate) -> AvailableDate | None:
        async with self.db.SessionLocal() as session:
            session.add(available_date)
            await session.commit()
            return available_date

    async def get_all_available_dates(self, month: int, year: int):
        async with self.db.SessionLocal() as session:
            return (await session.execute(
                select(AvailableDate).where(
                    extract('year', AvailableDate.event_date) == year,
                    extract('month', AvailableDate.event_date) == month
                ))).unique().scalars().all()

    async def delete_available_date(self, available_date: datetime.date):
        async with self.db.SessionLocal() as session:
            await session.execute(delete(AvailableDate).where(AvailableDate.event_date == available_date))
            await session.commit()
