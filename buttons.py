import json

from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
from aiogram.types import Message, ContentType
from aiogram.types import (
    ReplyKeyboardMarkup, # Нужен для обычной клавиатуры
    KeyboardButton, # Нужен для обычной клавиатуры
    InlineKeyboardMarkup, # Для инлайн клавиатуры
    InlineKeyboardButton, # Для инлайн клавиатуры
    ReplyKeyboardRemove
)


"""Вытаскиваем токен бота"""
def create_bot(config_file='token.json'):
    with open(config_file, 'r') as file:
        config = json.load(file)

    return Bot(token=config['token_bot'])

"""Создаем объекты бота и диспетчера"""
bot = create_bot()
dp = Dispatcher()

"""Обрабатываем меню"""
mein_menu = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="🎥 Поиск фильмов")],
        [KeyboardButton(text="📚 Избранное")],
        [KeyboardButton(text="🍿 Посмотреть позже"), KeyboardButton(text="⚙️ Настройки")]
    ],
    resize_keyboard=True
)


"""Обрабатываем команду start"""
@dp.message(Command(commands=["start"]))
async def process_start_command(message: Message):
    await message.answer(f"Привет. \nЯ телеграмм бот, который поможет тебе выбрать фильм для просмотра, "
                         f"по твоим критериям. Давай начнем.", reply_markup=mein_menu)


"""Обрабатываем команду help"""
@dp.message(Command(commands=["help"]))
async def process_help_command(message: Message):
    await message.answer(f"Выбери в меню раздел, который тебя интересует. Нажимай и переходи дальше",
                         reply_markup=mein_menu)


if __name__=="__main__":
    dp.run_polling(bot)