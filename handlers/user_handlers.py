
from aiogram import Router
from aiogram.filters import Command, CommandStart
from aiogram.types import Message
from lexicon.lexicon import LEXICON_RU
from config_data.config import load_config
from filters.auth import IsAuthUser
from keyboards.keyboards import keyboard
from aiogram.types import CallbackQuery
from aiogram import F

# from aiogram import Bot
# from keyboards.set_menu import set_main_menu, del_main_menu



# Инициализируем роутер уровня модуля
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
    await message.answer(text=LEXICON_RU['/start'], reply_markup=keyboard)
    # await set_main_menu(bot,MENU['2'])


# Этот хэндлер срабатывает на команду /help
@router.message(Command(commands='help'))
async def process_help_command(message: Message):
    await message.answer(text=LEXICON_RU['/help'])
    # await del_main_menu(bot)

@router.message(Command(commands='index1'))
async def process_help_command(message: Message):
    await message.answer(text=LEXICON_RU['/refresh_menu'])



@router.callback_query(F.data == 'big_button_1_pressed')
async def process_button_1_press(callback: CallbackQuery):
    if callback.message.text != 'Была нажата БОЛЬШАЯ КНОПКА 1':
        await callback.message.edit_text(
            text='Была нажата БОЛЬШАЯ КНОПКА 1',
            reply_markup=callback.message.reply_markup
        )
    await callback.answer()


# Этот хэндлер будет срабатывать на апдейт типа CallbackQuery
# с data 'big_button_2_pressed'
@router.callback_query(F.data == 'big_button_2_pressed')
async def process_button_2_press(callback: CallbackQuery):
    if callback.message.text != 'Была нажата БОЛЬШАЯ КНОПКА 2':
        await callback.message.edit_text(
            text='Была нажата БОЛЬШАЯ КНОПКА 2',
            reply_markup=callback.message.reply_markup
        )
    await callback.answer()