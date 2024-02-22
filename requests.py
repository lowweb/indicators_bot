from sqlalchemy import select

from models.models import Indicator
from models.models import async_session


async def add_row(async_session: async_session):
    test_row = Indicator(user=323, department='new', indicator=1)
    async with async_session() as session:
        session.add(test_row)
        await session.commit()
        return test_row

async def check_rows(async_session: async_session):
    async with async_session() as session:
        result = await session.scalars(select(Indicator))
        return result