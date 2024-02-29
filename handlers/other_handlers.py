from aiogram import Router
from aiogram.types import Message
from lexicon.lexicon import LEXICON_MSG
from aiogram.filters import Command, CommandStart
from keyboards.keyboards import create_inline_kb

# Инициализируем роутер уровня модуля
router = Router()

# Этот хэндлер будет срабатывать на любые ваши сообщения,
# кроме команд "/start" и "/help"


# @router.message(CommandStart())
# async def process_start_command(message: Message):
#     keyboard = create_inline_kb(1, DEFAULT_MENU)
#     await message.answer(text=LEXICON_MSG['/pleasereg'], reply_markup=keyboard)
#     # await set_main_menu(bot,MENU['2'])

# @router.callback_query()
# async def process_help_command(message: Message):
#     await message.answer(text=LEXICON_MSG['/afterreg'])


@router.message()
async def send_echo(message: Message):
    await message.answer(text=f'{LEXICON_MSG["/noreg"]} *{message.from_user.id}*',parse_mode= 'Markdown')

    #функиця получения отчета, пока положил сюда (если пользователь не зареган, то получает отчет)
    # file = await download_report()
    # await message.reply_document(document=BufferedInputFile(file=file.getvalue().encode('utf-8'), filename='report.csv'))

    # await message.answer(f'Ваш телеграмм ID {message.from_user.id}')
