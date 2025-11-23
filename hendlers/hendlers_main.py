from aiogram import F, Router, types
from aiogram.filters import Command, CommandStart, StateFilter
from aiogram import Router
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup, default_state
from aiogram.types import Message, ContentType

# Главное меню
# Создаём класс для группы состояний главного меню
class ChoiceOfFilms(StatesGroup):         # Выбор фильмов
    # Перечисляем возможные состояния главного меню
    first_choice = State()          # Состояние первого выбора в главном меню
    search_for_movies = State()     # Состояние кнопки "поиск фильмов"
    list_of_films = State()         # Состояние кнопки "список фильмов"

router = Router()
"""Обрабатываем команду start"""
# Этот хэндлер будет срабатывать на команду /start вне состояний и предлагать сделать выбор нажатия одной из кнопок
# главного меню
@router.message(CommandStart(), StateFilter(default_state))
async def process_start_command(message: Message):
    pass

"""Обрабатываем команду help"""
# Этот хэндлер будет срабатывать на команду /help в любых состояниях, кроме состояния по умолчанию и сообщать
# что вы можете сейчас сделать
@router.message(Command(commands="/help"), ~StateFilter(default_state))
async def process_help_command():
    pass

