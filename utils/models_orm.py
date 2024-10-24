from datetime import datetime, date, time
from sqlalchemy import ForeignKey, BigInteger, Integer, func
from sqlalchemy.orm import Mapped, mapped_column, DeclarativeBase, relationship

from utils.models import SlotStatus


class Base(DeclarativeBase):
    pass


class User(Base):
    __tablename__ = 'users'

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True)
    firstname: Mapped[str] = mapped_column(nullable=True)
    lastname: Mapped[str] = mapped_column(nullable=True)
    username: Mapped[str] = mapped_column()
    ban: Mapped[bool] = mapped_column(default=False)
    created: Mapped[datetime] = mapped_column(server_default=func.now())
    updated: Mapped[datetime] = mapped_column(server_default=func.now(), onupdate=func.now())

    def __repr__(self):
        return (f'User({self.id}, {self.firstname}, {self.lastname}, '
                f'{self.username}, {self.ban}, {self.created}, {self.updated})')


class Category(Base):
    __tablename__ = 'categories'

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column()
    text: Mapped[str] = mapped_column()
    items_in_category: Mapped[list['Item']] = relationship(back_populates='category')


class Item(Base):
    __tablename__ = 'items'

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column()
    price: Mapped[float] = mapped_column()
    description: Mapped[str] = mapped_column()
    image_path: Mapped[str] = mapped_column(nullable=True)
    category_id: Mapped[int] = mapped_column(Integer, ForeignKey('categories.id'))
    category: Mapped['Category'] = relationship(back_populates='items_in_category')


class OrderItem(Base):
    __tablename__ = 'order_items'

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True)
    user_id: Mapped[int] = mapped_column(BigInteger, ForeignKey('users.id'))
    item_id: Mapped[int] = mapped_column(ForeignKey('items.id'))
    item: Mapped['Item'] = relationship(lazy='joined')
    order_id: Mapped[int] = mapped_column(ForeignKey('orders.id'), nullable=True)
    order: Mapped['Order'] = relationship(back_populates='order_items')
    quantity: Mapped[int] = mapped_column()
    created: Mapped[datetime] = mapped_column(server_default=func.now())
    updated: Mapped[datetime] = mapped_column(server_default=func.now(), onupdate=func.now())

    def __repr__(self):
        return (f'OrderItem({self.id}, {self.user_id}, {self.item_id}, {self.order_id}, '
                f'{self.quantity}, {self.created}, {self.updated})')


class Order(Base):
    __tablename__ = 'orders'

    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(BigInteger, ForeignKey('users.id'))
    order_items: Mapped[list['OrderItem']] = relationship(back_populates='order', lazy='joined')
    status: Mapped[str] = mapped_column()
    created: Mapped[datetime] = mapped_column(server_default=func.now())
    updated: Mapped[datetime] = mapped_column(server_default=func.now(), onupdate=func.now())


class Event(Base):
    __tablename__ = 'planner_events'

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column()
    description: Mapped[str] = mapped_column()
    duration: Mapped[int] = mapped_column()


class SlotDate(Base):
    __tablename__ = 'planner_dates'

    id: Mapped[int] = mapped_column(primary_key=True)
    slot_date: Mapped[date] = mapped_column()
    published: Mapped[bool] = mapped_column(default=True)
    slots: Mapped[list['Slot']] = relationship(lazy='joined')

    def __repr__(self):
        return f'SlotDate(id={self.id}, slot_date={self.slot_date})'


class Slot(Base):
    __tablename__ = 'planner_slots'

    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(BigInteger, ForeignKey('users.id'))
    user: Mapped['User'] = relationship(lazy='joined')
    event_id: Mapped[int] = mapped_column(ForeignKey('planner_events.id'))
    event: Mapped['Event'] = relationship(lazy='joined')
    slot_date_id: Mapped[int] = mapped_column(ForeignKey('planner_dates.id'))
    slot_date: Mapped[SlotDate] = relationship(back_populates='slots', lazy='joined')
    start_time: Mapped[time] = mapped_column()
    status: Mapped[SlotStatus] = mapped_column()
    created: Mapped[datetime] = mapped_column(server_default=func.now())
    updated: Mapped[datetime] = mapped_column(server_default=func.now(), onupdate=func.now())

    def __repr__(self):
        return (f'Slot(id={self.id}, user_id={self.user_id}, event={self.event}, start_date={self.slot_date}, '
                f'start_time={self.start_time}, status={self.status}, created={self.created}, updated={self.updated})')
