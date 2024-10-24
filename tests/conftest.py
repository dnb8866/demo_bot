import asyncio
from datetime import datetime, timezone, date, time

import pytest

from engine import sql_db
from utils.models_orm import User, Slot, Event, SlotDate
from utils.repositories import UserRepository


@pytest.fixture(scope="session")
def event_loop():
    try:
        loop = asyncio.get_running_loop()
    except RuntimeError:
        loop = asyncio.new_event_loop()
    yield loop
    loop.close()


@pytest.fixture(scope='session')
def anyio_backend():
    return "asyncio"


@pytest.fixture(scope='session')
def db():
    return sql_db


@pytest.fixture(scope='session')
async def user_repo(db):
    return UserRepository(db)


@pytest.fixture
async def session(db):
    await db.clean()
    async with db.SessionLocal() as s:
        yield s
        await s.rollback()

@pytest.fixture(scope='session')
def dt():
    return datetime.now(timezone.utc)


@pytest.fixture
def user():
    return User(
        firstname='David',
        lastname='Smirnov',
        username='d_smirnov',
        ban=False
    )

@pytest.fixture
async def user_in_db(session, user):
    session.add(user)
    await session.commit()
    await session.refresh(user)
    return user


@pytest.fixture
def events():
    event_1 = Event(name='Прием', duration=90)
    event_2 = Event(name='Консультация', duration=120)
    event_3 = Event(name='Повторный прием', duration=45)
    return [event_1, event_2, event_3]


@pytest.fixture
def slots(events):
    slot_1 = Slot(event=events[0], slot_date=SlotDate(slot_date=date(2024, 1, 1)), start_time=time(10))
    slot_2 = Slot(event=events[1], slot_date=SlotDate(slot_date=date(2024, 1, 1)), start_time=time(13))
    slot_3 = Slot(event=events[2], slot_date=SlotDate(slot_date=date(2024, 1, 1)), start_time=time(17))
    slot_4 = Slot(event=events[0], slot_date=SlotDate(slot_date=date(2024, 1, 2)), start_time=time(12))
    return [slot_1, slot_2, slot_3, slot_4]