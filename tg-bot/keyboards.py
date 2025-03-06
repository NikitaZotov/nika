from aiogram.utils.keyboard import (InlineKeyboardBuilder, InlineKeyboardButton)
commands = ['Что такое Ника?', 'Стоп']


async def start_commands():
    keyboard = InlineKeyboardBuilder()
    for comm in commands:
        keyboard.add(InlineKeyboardButton(text=comm, callback_data=comm))
    return keyboard.adjust(1).as_markup()
