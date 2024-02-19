from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder

def create_inline_kb (width: int, menu_items: dict, prefix: str):
    kb_builder = InlineKeyboardBuilder()
    buttons: list[InlineKeyboardButton] = []
    for name, command in menu_items.items():
        buttons.append(InlineKeyboardButton(text=f'{name}', callback_data = f'{prefix}_{command}'))
    kb_builder.row(*buttons, width=width)
    return kb_builder.as_markup()

