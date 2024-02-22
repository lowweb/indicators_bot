import datetime

from sqlalchemy import select, delete
from database.models import Indicator, User, Data_indicator, Role
from database.models import async_session


async def get_user_id(tg_id: int) -> int:
    async with async_session() as session:
        user_id = await session.scalar(select(User.id).where(User.tg_id == tg_id))
        return user_id

async def get_role_id(tg_id: int) -> int:
    async with async_session() as session:
        user_id = await session.scalar(select(User.role_id).where(User.tg_id == tg_id))
        return user_id

#Получаем словарь всего списка показаний по конкретнойроли
async def get_all_indicators_by_role(role_id: int) -> dict:
    async with async_session() as session:
        indicators = await session.scalars(select(Indicator).where(Indicator.role_id == role_id))
        result = {res.name: res.id for res in indicators}
        return result


#Добавление показания по выбранному indicator_id
async def add_user_data_indicator(indicator_id, indicator_value, user_id):
    async with async_session() as session:
        indicator_row = Data_indicator(indicator_id=indicator_id, indicator_value=indicator_value, user_id=user_id)
        session.add(indicator_row)
        await session.commit()
        return indicator_row

#Удаление по indicator_id
async def delete_user_data_indicator(indicator_id):
    async with async_session() as session:
        delete_id = await session.scalar(select(Data_indicator).where(Data_indicator.id == indicator_id))
        await session.delete(delete_id)
        await session.commit()
        return delete_id
    

# Получения словаря всех сделаных показаний по конкретному юзеру
async def get_users_data_indicators(indicator_id: int, user_id: int, days):
    one_month = datetime.timedelta(days=days)
    month_ago = datetime.datetime.now() - one_month
    async with async_session() as session:
        users_data_indicators = await session.scalars(
            select(Data_indicator).where(Data_indicator.indicator_id == indicator_id).where(Data_indicator.user_id == user_id).where(
                Data_indicator.created_at > month_ago))
        user_data = {f'{data.created_at.strftime("%m/%d/%Y %H:%M")} {data.indicator_value}': data.id for data in
                     users_data_indicators}
        return user_data
    


# Обновление показаний по id
async def update_user_data_indicators(data_indicator_id, user_id, update_data):
    async with async_session() as session:
        user_data_indicator = await session.scalar(
            select(Data_indicator).where(Data_indicator.id == data_indicator_id).where(
                Data_indicator.user_id == user_id))
        user_data_indicator.indicator_value = update_data
        await session.commit()
        return user_data_indicator



# async def add_role():
#     role = Role(name='Статистиа')
#     async with async_session() as session:
#         session.add(role)
#         await session.commit()
#         return role

# async def add_user():
#     test_row = User(name='Морев', tg_id=561132, role_id='1')
#     async with async_session() as session:
#         session.add(test_row)
#         await session.commit()
#         return test_row



# async def add_indicator():
#     indicator = Indicator(name='Средний КЗ', role_id=2, periodicity=1)
#     async with async_session() as session:
#         session.add(indicator)
#         await session.commit()
#         return indicator
