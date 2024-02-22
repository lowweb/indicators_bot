import datetime

from sqlalchemy import select, delete
from database.models import Indicator, User, Data_indicator, Role
from database.models import async_session


#Получаем словарь всего списка показаний по конкретнойроли
async def get_all_indicators_by_role(role_id: int) -> dict:
    async with async_session() as session:
        indicators = await session.scalars(select(Indicator).where(Indicator.role_id == role_id))
        result = {res.name: res.id for res in indicators}
        print(result)
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
        print(f'del= {delete_id}')
        await session.delete(delete_id)
        await session.commit()
        print(delete_id)
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

# async def set_user(tg_id):
#     async with async_session() as session:
#         user = await session.scalar(select(User).where(User.tg_id == tg_id))
#
#         if not user:
#             session.add(User(tg_id=tg_id))
#             await session.commit()


# async def add_user():
#     test_row = User(name='Морев', tg_id=561132)
#     async with async_session() as session:
#         session.add(test_row)
#         await session.commit()
#         return test_row
#
# async def add_role():
#     role = Role(role=2, user_id=2)
#     async with async_session() as session:
#         session.add(role)
#         await session.commit()
#         return role
#
#
# async def add_indicator():
#     indicator = Indicator(name='Средний КЗ', role_id=2, periodicity=1)
#     async with async_session() as session:
#         session.add(indicator)
#         await session.commit()
#         return indicator

# async def add_data_indicator(message: Message, indicator_id):
#     async with async_session() as session:
#         data_indicator = Data_indicator(indicator_id=indicator_id, indicator_value=message.text,
#                                         user_id=message.from_user.id)
#         session.add(data_indicator)
#         await session.commit()
#         return data_indicator


# async def get_all_indicators_by_role():
#     async with async_session() as session:
#         indicators = await session.scalars(select(Indicator))
#         result = {res.id: res.name for res in indicators}
#         print(result)
#         return result


# Клава под него!
# async def indicators():
#     all_indicators = await get_all_indicators()
#     keyboard = InlineKeyboardBuilder()
#     for indicator in all_indicators:
#         keyboard.add(InlineKeyboardButton(text=indicator.name,
#                                           callback_data=f'category_{indicator.id}'))
#     keyboard.add(InlineKeyboardButton(text='Назад', callback_data='Главная'))
#     return keyboard.adjust(2).as_markup()
