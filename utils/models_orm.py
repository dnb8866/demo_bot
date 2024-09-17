from datetime import datetime
from uuid import UUID
from sqlalchemy import ForeignKey, BigInteger, Integer
from sqlalchemy.orm import Mapped, mapped_column, DeclarativeBase, relationship


class Base(DeclarativeBase):
    pass


class User(Base):
    __tablename__ = 'users'

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True)
    firstname: Mapped[str] = mapped_column(nullable=True)
    lastname: Mapped[str] = mapped_column(nullable=True)
    username: Mapped[str] = mapped_column(nullable=True)
    ban: Mapped[bool] = mapped_column(default=False)
    created: Mapped[datetime] = mapped_column()
    updated: Mapped[datetime] = mapped_column()

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
    item: Mapped['Item'] = relationship()
    order_id: Mapped[UUID] = mapped_column(ForeignKey('orders.id'), nullable=True)
    order: Mapped['Order'] = relationship(back_populates='order_items')
    quantity: Mapped[int] = mapped_column()
    created: Mapped[datetime] = mapped_column()
    updated: Mapped[datetime] = mapped_column()

    def __repr__(self):
        return f'OrderItem({self.id}, {self.user_id}, {self.item_id}, {self.order_id}, {self.quantity})'


class Order(Base):
    __tablename__ = 'orders'

    id: Mapped[UUID] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(BigInteger, ForeignKey('users.id'))
    order_items: Mapped[list['OrderItem']] = relationship(back_populates='order')
    status: Mapped[str] = mapped_column()
    created: Mapped[datetime] = mapped_column()
    updated: Mapped[datetime] = mapped_column()
