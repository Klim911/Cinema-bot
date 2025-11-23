from aiogram import F, Router, types
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.types import Message, ContentType

# Посик фильмов
# Создаём класс дял группы состояний внутри кнопки поиска фильма
class Categories(StatesGroup):          # Категории
    select_year = State()               # Состояние ожидания выбора года
    select_genre = State()              # Состояние ожидания выбора жанра
    select_rating = State()             # Состояние ожидания выбора рейтинга
    select_time = State()               # Состояние ожидания выбора времени просмотра
    select_review = State()             # Состояние ожидания выбора обзора фильма
    select_sorting_rating = State()     # Состояние ожидания выбора сортировки по рейтингу
    select_sorting_likes = State()      # Состояние ожидания выбора сортировки по лайкам


