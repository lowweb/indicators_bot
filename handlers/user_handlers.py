
from aiogram import Router
from aiogram.filters import Command, CommandStart
from aiogram.types import Message
from lexicon.lexicon import LEXICON_RU
from config_data.config import load_config
from filters.auth import IsAuthUser
from keyboards.keyboards import yes_no_kb



# Инициализируем роутер уровня модуля
router = Router()

config = load_config()
AUTH_IDS = config.tg_bot.users_ids


router.message.filter(IsAuthUser(AUTH_IDS))
# print(type(AUTH_IDS))
# print(AUTH_IDS)
# print(IsAuthUser(AUTH_IDS))

# Этот хэндлер срабатывает на команду /start

@router.message(CommandStart())
async def process_start_command(message: Message):
    await message.answer(text=LEXICON_RU['/start'])


# Этот хэндлер срабатывает на команду /help
@router.message(Command(commands='help'))
async def process_help_command(message: Message):
    await message.answer(text=LEXICON_RU['/help'])

@router.message(Command(commands='refresh_menu'))
async def process_help_command(message: Message):
    await message.answer(text=LEXICON_RU['/refresh_menu'])    