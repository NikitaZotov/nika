from aiogram import Bot, Dispatcher, types
from aiogram import F
from aiogram.filters import Command
from aiogram.fsm.storage.memory import MemoryStorage

import keyboards as kb
from html_parser import html_to_telegram_text
from nika_utils import get_nika_response

bot = Bot(token='7725642650:AAHYT-_c2JUgAAMCTduGImqxK8qbRyYAZlc')
storage = MemoryStorage()
dp = Dispatcher(storage=storage)


@dp.message(Command("start"))
async def start(message: types.Message):
    text = '''
    ㅤ\n
    Добро пожаловать в NIKA!

    Мы рады видеть вас в нашей системе. Здесь вы сможете легко общаться с системой через интерфейс телеграм-бота.

    Если у вас есть вопросы или нужна помощь, не стесняйтесь обращаться. Я всегда готова помочь!\n
    ㅤ\n
    '''

    await message.answer(text, parse_mode='HTML',
                         reply_markup=await kb.start_commands())


# @dp.callback_query(F.data == 'Что умеет Ника?')
# async def callback(message: types.Message):
#     text = get_nika_response('Что умеет Ника?')
#     await message.answer(text, parse_mode='HTML', )


@dp.message(F.text)
async def handle_message(message: types.Message):
    user_message = message.text
    nika_response = get_nika_response(user_message)
    result_response = html_to_telegram_text(nika_response)
    await message.answer(result_response)


@dp.message(Command("info"))
async def info(message: types.Message):
    info_text = (
        "Сюда я добавлю информацию о системе NIKA"
    )
    await message.answer(info_text)
