from aiogram import F, Router, types
from aiogram.filters import StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup, default_state
from aiogram.types import Message, ContentType

from hendlers_main import ChoiceOfFilms

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


search_router = Router()

# Этот хэендлер будет срабатывать, если нажата кнопка "Поиск фильма" и переводить в состояние
# ожидания выбора года
@search_router.message(StateFilter(ChoiceOfFilms.first_choice))
async def process_select_year_command(state: FSMContext):
    pass
    # Устанавливаем состояние выбора года
    await state.set_state(Categories.select_year)


# Этот хэндлер будет срабатывать если выбран один из годов и переводить в состояние выбора жанра
@search_router.message(StateFilter(Categories.select_year))
async def process_select_genre_command(state: FSMContext):
    pass
    # Устанавливаем состояние выбора жанра
    await state.set_state(Categories.select_genre)


# Этот хэндлер будет срабатывать если выбран один из жанров и переводить в состояние выбора рейтинга
@search_router.message(StateFilter(Categories.select_genre))
async def process_select_genre_command(state: FSMContext):
    pass
    # Устанавливаем состояние выбора рейтинга
    await state.set_state(Categories.select_rating)


# Этот хэндлер будет срабатывать если выбран рейтинг и переводить в состояние выбора времени просмотра
@search_router.message(StateFilter(Categories.select_rating))
async def process_select_time_command(state: FSMContext):
    pass
    # Устанавливаем состояние выбора времени просмотра
    await state.set_state(Categories.select_time)


# Этот хэндлер будет срабатывать если выбрано время просмотра и переводить в ???
@search_router.message(StateFilter(Categories.select_time))
async def process_select_review_command(state: FSMContext):
    pass
