import datetime as dt
import pytest
from sqlalchemy import select, update, delete
from sqlalchemy.dialects.postgresql import insert

from config import SQLALCHEMY_DATABASE_URL_TEST
from utils.db import AlchemySqlDb
from utils.models_orm import Base, User
from utils.repositories import UserRepository


class TestDb:

    db = AlchemySqlDb(SQLALCHEMY_DATABASE_URL_TEST, Base, test=True)
    dt_now = dt.datetime.utcnow()

    @pytest.mark.asyncio
    async def test_clean(self):
        await self.db.clean()
        async with self.db.SessionLocal() as session:
            res = (await session.execute(select(User))).all()
            assert len(res) == 0, "Test cleaning failed"

    @pytest.mark.asyncio
    async def test_prepare(self):
        await self.db.prepare()

    @pytest.mark.asyncio
    async def test_insert(self):
        async with self.db.SessionLocal() as session:
            await session.execute(insert(User).values(firstname='Petr', created=self.dt_now, updated=self.dt_now))
            await session.commit()

    @pytest.mark.asyncio
    async def test_get(self):
        async with self.db.SessionLocal() as session:
            res = (await session.execute(select(User).where(User.firstname == 'Petr'))).scalar_one_or_none()
            assert res is not None

    @pytest.mark.asyncio
    async def test_update(self):
        async with self.db.SessionLocal() as session:
            await session.execute(update(User).where(User.firstname == 'Petr').values(firstname='Peter'))
            await session.commit()
            res = (await session.execute(select(User).where(User.firstname == 'Peter'))).scalar_one_or_none()
            assert res.firstname == 'Peter'

    @pytest.mark.asyncio
    async def test_delete(self):
        async with self.db.SessionLocal() as session:
            await session.execute(delete(User).where(User.firstname == 'Peter'))
            await session.commit()
            res = (await session.execute(select(User).where(User.firstname == 'Peter'))).scalar_one_or_none()
            assert res is None


class TestUserRepository:
    db = AlchemySqlDb(SQLALCHEMY_DATABASE_URL_TEST, Base, test=True)
    repo = UserRepository(db)
    user = User(
        id=1,
        firstname='John',
        lastname='Smith',
        username='jsmith',
        ban=False,
        created=dt.datetime.utcnow(),
        updated=dt.datetime.utcnow())

    @pytest.mark.asyncio
    async def test_add(self):
        await self.repo.add(self.user)

    @pytest.mark.asyncio
    async def test_get(self):
        user = await self.repo.get(self.user.id)
        assert (user.id, user.username, user.created) == (self.user.id, self.user.username, self.user.created)
