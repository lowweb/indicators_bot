from datetime import datetime
from typing import List

from sqlalchemy import ForeignKey, String
from sqlalchemy.orm import relationship, Mapped, mapped_column, DeclarativeBase, backref
from sqlalchemy.ext.asyncio import AsyncAttrs, async_sessionmaker, create_async_engine
from sqlalchemy.sql.functions import now

engine = create_async_engine('sqlite+aiosqlite:///database/db.sqlite3')

async_session = async_sessionmaker(engine)


class Base(AsyncAttrs, DeclarativeBase):
    pass


class User(Base):
    __tablename__ = 'users'

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(50))
    tg_id: Mapped[int] = mapped_column()
    data_indicators: Mapped[List['Data_indicator']] = relationship(back_populates='users')

class Role(Base):
    __tablename__ = 'roles'
    id: Mapped[int] = mapped_column(primary_key=True)
    role: Mapped[int] = mapped_column()
    user_id: Mapped[int] = mapped_column(ForeignKey('users.id'))
    indicators: Mapped[List['Indicator']] = relationship(back_populates='roles')


class Indicator(Base):
    __tablename__ = 'indicators'

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(70))
    role_id: Mapped[int] = mapped_column(ForeignKey('roles.id'))
    periodicity: Mapped[int] = mapped_column()
    roles: Mapped['Role'] = relationship(back_populates='indicators')

class Data_indicator(Base):
    __tablename__ = 'data_indicators'

    id: Mapped[int] = mapped_column(primary_key=True)
    indicator_id: Mapped[int] = mapped_column(ForeignKey("indicators.id"))
    indicator_value: Mapped[int] = mapped_column()
    created_at: Mapped[datetime] = mapped_column(server_default=now())
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    users: Mapped['User'] = relationship(back_populates='data_indicators')


async def create_db():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
