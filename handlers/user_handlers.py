
from aiogram import Router
from aiogram.filters import Command, CommandStart
from aiogram.types import Message
from lexicon.lexicon import LEXICON_MSG,LEXICON_PREFIX
from api.data import MENU_ITEMS,EDIT_MENU_ITEMS,UPDATE_MENU_ITEMS
from config_data.config import load_config
from filters.auth import IsAuthUser
from keyboards.keyboards import create_inline_kb
from aiogram.types import CallbackQuery
from aiogram import F
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from services.services import get_value_by_key 


class Form(StatesGroup):
    new_answer = State()
    new_title = State()
    edit_title = State()
    update_answer = State()
    update_title = State()
    update_id = State()

router = Router()

config = load_config()
AUTH_IDS = config.tg_bot.users_ids
# bot = Bot(token=config.tg_bot.token)

router.message.filter(IsAuthUser(AUTH_IDS))
# print(type(AUTH_IDS))
# print(AUTH_IDS)
# print(IsAuthUser(AUTH_IDS))

# Этот хэндлер срабатывает на команду /start
@router.message(CommandStart())
async def process_start_command(message: Message):
    # запрос
    keyboard = create_inline_kb(1, MENU_ITEMS, LEXICON_PREFIX['new'])
    await message.answer(text=LEXICON_MSG['/start'], reply_markup=keyboard)
    # await set_main_menu(bot,MENU['2'])


# Этот хэндлер срабатывает на yнажатие внесения показателя   
@router.callback_query(F.data.startswith(LEXICON_PREFIX['new']))
async def process_category_press(callback: CallbackQuery,state: FSMContext):
    await state.set_state(Form.new_answer)
    # await state.update_data(new_title=callback.data.split('_')[1])
    value = get_value_by_key(callback.data.split('_')[1], MENU_ITEMS)
    await callback.message.answer(text=f"Введите значение показателя {value}")
    await callback.answer()

# ответ при вводе показателя
@router.message(Form.new_answer)
async def process_state(message: Message, state: FSMContext) -> None:
    await state.update_data(new_answer=message.text)
    await state.clear()
    keyboard = create_inline_kb(1, MENU_ITEMS, LEXICON_PREFIX['new'])
    await message.answer(
        f"Значение= {message.text}!\nзаписанно в БД", reply_markup=keyboard
    )    

@router.message(Command(commands='edit_indicators'))
async def process_start_command(message: Message):
    keyboard = create_inline_kb(1, EDIT_MENU_ITEMS, LEXICON_PREFIX['edit'])
    await message.answer(text=LEXICON_MSG['/edit_indicators'], reply_markup=keyboard)


# Этот хэндлер срабатывает на меню редактирование показателя 
@router.callback_query(F.data.startswith(LEXICON_PREFIX['edit']))
async def process_category_press(callback: CallbackQuery,state: FSMContext):
    keyboard = create_inline_kb(2, UPDATE_MENU_ITEMS, LEXICON_PREFIX['update'])
    value = get_value_by_key(callback.data.split('_')[1], EDIT_MENU_ITEMS)
    await callback.message.answer(text=f"{value}",reply_markup=keyboard)
    await callback.answer() 

# Этот хэндлер срабатывает на нажатие кнопки обновляемого показателя  
@router.callback_query(F.data.startswith(LEXICON_PREFIX['update']))
async def category(callback: CallbackQuery, state: FSMContext):
    await state.set_state(Form.update_answer)
    await state.update_data(update_id=callback.data.split('_')[1])
    value = get_value_by_key(callback.data.split('_')[1], EDIT_MENU_ITEMS)
    await callback.message.answer(text=f"Введите значение для редактируемого показателя {value}")
    await callback.answer('')

# ответ при вводе показателя для обновленя
@router.message(Form.update_answer)
async def process_state(message: Message, state: FSMContext) -> None:
    await state.update_data(update_answer=message.text)
    id= await state.get_data()
    await state.clear()
    await message.answer(
        f"Значение= {id['update_id']}!\nотредактированно")   
     

@router.message()
async def send_echo(message: Message):
    await message.answer(text=LEXICON_MSG['/waitinput'])    
    

# Этот хэндлер срабатывает на команду /help
@router.message(Command(commands='help'))
async def process_help_command(message: Message):
    await message.answer(text=LEXICON_MSG['/help'])
    # await del_main_menu(bot)