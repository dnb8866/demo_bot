import datetime as dt
import pytest
from sqlalchemy import select, update, delete
from sqlalchemy.dialects.postgresql import insert

from config import SQLALCHEMY_SHOP_DB_URL_TEST
from planner.entities import Day
from utils.constants import PLANNER_DAY_SCHEDULE
from utils.db import AlchemySqlDb
from utils.models_orm import Base, User, Event, Slot, SlotDate
from utils.repositories import UserRepository


class TestDb:
    # TODO: need refactoring
    db = AlchemySqlDb(SQLALCHEMY_SHOP_DB_URL_TEST, Base, test=True)
    dt_now = dt.datetime.utcnow()

    async def test_clean(self):
        await self.db.clean()
        async with self.db.SessionLocal() as session:
            res = (await session.execute(select(User))).all()
            assert len(res) == 0, "Test cleaning failed"

    async def test_prepare(self):
        await self.db.prepare()

    async def test_insert(self):
        async with self.db.SessionLocal() as session:
            await session.execute(insert(User).values(firstname='Petr', created=self.dt_now, updated=self.dt_now))
            await session.commit()

    async def test_get(self):
        async with self.db.SessionLocal() as session:
            res = (await session.execute(select(User).where(User.firstname == 'Petr'))).scalar_one_or_none()
            assert res is not None

    async def test_update(self):
        async with self.db.SessionLocal() as session:
            await session.execute(update(User).where(User.firstname == 'Petr').values(firstname='Peter'))
            await session.commit()
            res = (await session.execute(select(User).where(User.firstname == 'Peter'))).scalar_one_or_none()
            assert res.firstname == 'Peter'

    async def test_delete(self):
        async with self.db.SessionLocal() as session:
            await session.execute(delete(User).where(User.firstname == 'Peter'))
            await session.commit()
            res = (await session.execute(select(User).where(User.firstname == 'Peter'))).scalar_one_or_none()
            assert res is None


class TestUserRepository:
    # TODO: need refactoring
    db = AlchemySqlDb(SQLALCHEMY_SHOP_DB_URL_TEST, Base, test=True)
    repo = UserRepository(db)
    user = User(
        id=1,
        firstname='John',
        lastname='Smith',
        username='jsmith',
        ban=False,
        created=dt.datetime.utcnow(),
        updated=dt.datetime.utcnow())

    async def test_add(self):
        await self.repo.add(self.user)

    async def test_get(self):
        user = await self.repo.get(self.user.id)
        assert (user.id, user.username, user.created) == (self.user.id, self.user.username, self.user.created)


class TestPlanner:
    event_1 = Event(name='event_1', duration=90)
    event_2 = Event(name='event_2', duration=120)
    event_3 = Event(name='event_3', duration=45)

    date_1 = SlotDate(slot_date=dt.date(2024, 1, 1))
    date_2 = SlotDate(slot_date=dt.date(2024, 1, 2))

    slot_1 = Slot(event=event_1, slot_date=date_1, start_time=dt.time(10))
    slot_2 = Slot(event=event_2, slot_date=date_1, start_time=dt.time(13))
    slot_3 = Slot(event=event_3, slot_date=date_1, start_time=dt.time(17))
    slot_4 = Slot(event=event_1, slot_date=date_2, start_time=dt.time(12))

    def test_day_schedule(self):
        day = Day([self.slot_1, self.slot_2, self.slot_3])
        assert day.schedule == {
            dt.time(9, 0): None,
            dt.time(9, 30): None,
            dt.time(10, 0): self.slot_1,
            dt.time(11, 30): None,
            dt.time(12, 0): None,
            dt.time(12, 30): None,
            dt.time(13, 0): self.slot_2,
            dt.time(15, 0): None,
            dt.time(15, 30): None,
            dt.time(16, 0): None,
            dt.time(16, 30): None,
            dt.time(17, 0): self.slot_3
        }

    def test_check_many_dates(self):
        with pytest.raises(ValueError, match='Список слотов содержит более 1 даты.'):
            Day([self.slot_1, self.slot_2, self.slot_3, self.slot_4])

    def test_check_no_date(self):
        day = Day([])
        assert day.schedule == PLANNER_DAY_SCHEDULE
