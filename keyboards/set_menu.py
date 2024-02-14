from aiogram import Bot
from aiogram.types import BotCommand

# from lexicon.lexicon import LEXICON_MENU


async def del_main_menu(bot: Bot):
    await bot.delete_my_commands()
# 
# Функция для настройки кнопки Menu бота
async def set_main_menu(bot: Bot, menu):
    main_menu_commands = [
        BotCommand(
            command=command,
            description=description
        ) for command, description in menu.items()
    ]
    await bot.set_my_commands(main_menu_commands)

