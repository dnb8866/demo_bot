from sqlalchemy import select, update, delete
from sqlalchemy.dialects.postgresql import insert

from utils.models_orm import User


class TestDb:

    async def test_insert(self, session, dt):
        users = set((await session.execute(select(User))).all())
        await session.execute(insert(User).values(firstname='Petr', username='petr'))
        await session.commit()
        assert len(set((await session.execute(select(User))).all()) - users) == 1

    async def test_get(self, session, user_in_db):
        user = (await session.execute(select(User).where(User.id == user_in_db.id))).scalar_one_or_none()
        assert user == user_in_db

    async def test_update(self, session, user_in_db):
        await session.execute(update(User).where(User.id == user_in_db.id).values(firstname='Peter'))
        await session.commit()
        user = (await session.execute(select(User).where(User.id == user_in_db.id))).scalar_one_or_none()
        assert user.firstname == 'Peter'

    async def test_delete(self, session, user_in_db):
        users = set((await session.execute(select(User))).all())
        await session.execute(delete(User).where(User.id == user_in_db.id))
        await session.commit()
        user = (await session.execute(select(User).where(User.id == user_in_db.id))).scalar_one_or_none()
        assert user is None
        assert len(users - set((await session.execute(select(User))).all())) == 1


class TestUserRepository:

    async def test_add(self, user_repo, user, session):
        await user_repo.add(user)
        user_from_session = (await session.execute(select(User).where(User.id == user.id))).scalar_one_or_none()
        assert user_from_session is not None
        assert user_from_session.firstname == user.firstname
        assert user_from_session.lastname == user.lastname
        assert user_from_session.username == user.username
        assert user_from_session.ban == user.ban

    async def test_get(self, user_repo, user_in_db, session):
        user_from_session = await user_repo.get(user_in_db.id)
        user_in_db.__dict__.pop('_sa_instance_state')
        user_from_session.__dict__.pop('_sa_instance_state')
        assert user_from_session.__dict__ == user_in_db.__dict__

    async def test_update(self, user_repo, user_in_db):
        user_in_db.firstname = 'Peter'
        user_from_session = await user_repo.update(user_in_db)
        assert user_from_session.firstname == user_in_db.firstname
        assert user_from_session.created == user_in_db.created
        assert user_from_session.updated != user_in_db.updated

    async def test_delete(self, user_repo, session, user_in_db):
        users = set(await session.execute(select(User)))
        await user_repo.delete(user_in_db.id)
        assert len(users - set(await session.execute(select(User)))) == 1
