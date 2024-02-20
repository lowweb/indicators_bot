
from aiogram import Router, Bot
from aiogram.filters import Command, CommandStart
from aiogram.types import Message
from lexicon.lexicon import LEXICON_MSG,LEXICON_PREFIX
from api.data import MENU_ITEMS,EDIT_MENU_ITEMS,UPDATE_MENU_ITEMS,DELETE_MENU_ITEMS
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
    delete_title =State()
    update_answer = State()
    update_title = State()
    update_id = State()

router = Router()
config = load_config()
AUTH_IDS = config.tg_bot.users_ids
bot = Bot(token=config.tg_bot.token)
router.message.filter(IsAuthUser(AUTH_IDS))

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
    new_title = get_value_by_key(callback.data.split('_')[1], MENU_ITEMS)
    await state.update_data(new_title=new_title)
    new_id = callback.data.split('_')[1]
    await state.update_data(new_id=new_id)
    await callback.message.answer(text=f"Введите значение показателя\n*{new_title}*",parse_mode= 'Markdown')
    await callback.answer()

# ответ при вводе показателя
@router.message(Form.new_answer, lambda x: x.text.isdigit())
async def process_state(message: Message, state: FSMContext) -> None:
    await state.update_data(new_answer=message.text)
    await state.clear()
    keyboard = create_inline_kb(1, MENU_ITEMS, LEXICON_PREFIX['new'])
    await message.answer(
        f"Данные = *{message.text}*, записанны. \nВыберите показатель, для передачи данных", reply_markup=keyboard,parse_mode= 'Markdown'
    )

@router.message(Form.new_answer)
async def process_state(message: Message, state: FSMContext) -> None:
    data = await state.get_data()
    await message.answer(text=f"Введите цифровое значение для показателя \n*{data['new_title']}*",parse_mode= 'Markdown')         

@router.message(Command(commands='edit_indicators'))
async def process_start_command(message: Message):
    keyboard = create_inline_kb(1, EDIT_MENU_ITEMS, LEXICON_PREFIX['edit'])
    await message.answer(text=LEXICON_MSG['/edit_indicators'], reply_markup=keyboard)


# Этот хэндлер срабатывает на меню редактирование показателя 
@router.callback_query(F.data.startswith(LEXICON_PREFIX['edit']))
async def process_category_press(callback: CallbackQuery,state: FSMContext):
    keyboard = create_inline_kb(2, UPDATE_MENU_ITEMS, LEXICON_PREFIX['update'])
    edit_title = get_value_by_key(callback.data.split('_')[1], EDIT_MENU_ITEMS)
    await state.update_data(edit_title=edit_title)
    await callback.message.answer(text=f"*{edit_title}*",reply_markup=keyboard,parse_mode= 'Markdown')
    await callback.answer() 

# Этот хэндлер срабатывает на нажатие кнопки обновляемого показателя  
@router.callback_query(F.data.startswith(LEXICON_PREFIX['update']))
async def category(callback: CallbackQuery, state: FSMContext):
    await state.set_state(Form.update_answer)
    update_title = get_value_by_key(callback.data.split('_')[1], UPDATE_MENU_ITEMS)
    await state.update_data(update_id=callback.data.split('_')[1])
    await state.update_data(update_title=update_title)
    data = await state.get_data()
    await callback.message.answer(text=f"Введите значение на которое следует обновить показатель \n*{data['update_title']}*",parse_mode= 'Markdown')
    await callback.answer('')

# ответ при вводе показателя для обновленя
@router.message(Form.update_answer, lambda x: x.text.isdigit())
async def process_state(message: Message, state: FSMContext) -> None:
    await state.update_data(update_answer=message.text)
    data = await state.get_data()
    await state.clear()
    await message.answer(
        f"Значение показателя *{data['edit_title']}* за *{data['update_title']}* измененно на *{data['update_answer']}*",parse_mode= 'Markdown')   

# ответ при вводе показателя для обновленя
@router.message(Form.update_answer)
async def process_state(message: Message, state: FSMContext) -> None:
    data = await state.get_data()
    await message.answer(text=f"Введите цифровое значение для обновляемого показателя \n *{data['update_title']}*",parse_mode= 'Markdown')   


@router.message(Command(commands='delete_indicators'))
async def process_delete_command(message: Message):
    keyboard = create_inline_kb(1, EDIT_MENU_ITEMS, LEXICON_PREFIX['delete'])
    await message.answer(text=LEXICON_MSG['/delete_indicators'], reply_markup=keyboard)

# Этот хэндлер срабатывает на меню редактирование показателя 
@router.callback_query(F.data.startswith(LEXICON_PREFIX['delete']))
async def process_delete_press(callback: CallbackQuery,state: FSMContext):
    keyboard = create_inline_kb(2, DELETE_MENU_ITEMS, LEXICON_PREFIX['itmdelete'])
    delete_title = get_value_by_key(callback.data.split('_')[1], EDIT_MENU_ITEMS)
    await state.update_data(delete_title=delete_title)
    await callback.message.answer(text=f"*{delete_title}*",reply_markup=keyboard,parse_mode= 'Markdown')
    await callback.answer()     

# Этот хэндлер срабатывает на нажатие кнопки обновляемого показателя  
@router.callback_query(F.data.startswith(LEXICON_PREFIX['itmdelete']))
async def category(callback: CallbackQuery, state: FSMContext):
    delete_title = get_value_by_key(callback.data.split('_')[1], DELETE_MENU_ITEMS)
    await state.update_data(delete_title=delete_title)
    data = await state.get_data()
    await state.clear()
    await callback.message.answer(text=f"Показатель *{data['delete_title']}* удален.",parse_mode= 'Markdown')
    await callback.answer('')

@router.message()
async def send_echo(message: Message):
    await message.answer(text=LEXICON_MSG['/waitinput'])    
    
# Этот хэндлер срабатывает на команду /help
@router.message(Command(commands='help'))
async def process_help_command(message: Message):
    await message.answer(text=LEXICON_MSG['/help'])
    # await del_main_menu(bot)

  