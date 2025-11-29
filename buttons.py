# import json
# from environs import Env
# from aiogram import Bot, Dispatcher, types
# from aiogram.filters import Command, CommandStart
# from aiogram.types import Message, ContentType
# from aiogram.types import (
#     ReplyKeyboardMarkup, # Нужен для обычной клавиатуры
#     KeyboardButton, # Нужен для обычной клавиатуры
#     InlineKeyboardMarkup, # Для инлайн клавиатуры
#     InlineKeyboardButton, # Для инлайн клавиатуры
#     ReplyKeyboardRemove
# )
#
#
# """Вытаскиваем токен бота"""
# # def create_bot(config_file='token.json'):
# #     with open(config_file, 'r') as file:
# #         config = json.load(file)
# #     return Bot(token=config['token_bot'])
# env = Env()
# env.read_env()
#
# bot_token = env('BOT_TOKEN')
#
# """Вытаскиваем список фильмов"""
#
#
# """Создаем объекты бота и диспетчера"""
# bot = Bot(token=bot_token)
# dp = Dispatcher()
#
# """Обрабатываем меню"""
# mein_menu = ReplyKeyboardMarkup(
#     keyboard=[
#         [KeyboardButton(text="🎥 Поиск фильмов")],
#         [KeyboardButton(text="📚 Избранное")],
#         [KeyboardButton(text="🍿 Посмотреть позже"), KeyboardButton(text="⚙️ Настройки")]
#     ],
#     resize_keyboard=True
# )
#
#
# """Обрабатываем команду start"""
# @dp.message(CommandStart())
# async def process_start_command(message: Message):
#     await message.answer(f"Привет. \nЯ телеграмм бот, который поможет тебе выбрать фильм для просмотра, "
#                          f"по твоим критериям. Давай начнем.", reply_markup=mein_menu)
#
#
# """Обрабатываем команду help"""
# @dp.message(Command(commands=["help"]))
# async def process_help_command(message: Message):
#     await message.answer(f"Выбери в меню раздел, который тебя интересует. Нажимай и переходи дальше",
#                          reply_markup=mein_menu)
#
# """Обработка клавиш нашего меню"""
# @dp.message(lambda message: message.text in ["🎥 Поиск фильмов", "📚 Избранное", "🍿 Посмотреть позже", "⚙️ Настройки"])
# async def handle_menu_buttons(message: Message):
#     if message.text == "🎥 Поиск фильмов":
#         # Новое меню для поиска
#         search_menu = ReplyKeyboardMarkup(
#             keyboard=[
#                 [KeyboardButton(text="🔍 По жанру")],
#                 [KeyboardButton(text="📰 По отзывам")],
#                 [KeyboardButton(text="🗓️ По году")]
#             ],
#             resize_keyboard=True
#         )
#         await message.answer(f"Как будем искать фильм?", reply_markup=search_menu)
#
#
# if __name__=="__main__":
#     dp.run_polling(bot)