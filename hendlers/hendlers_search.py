from aiogram import F, Router, types
from aiogram.filters import StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup, default_state
from aiogram.types import Message, ContentType

from states import GeneralConditions
from lexicon.lexicon import LEXICON
from keyboards.keyboards import *



search_router = Router()

# Этот хэендлер будет срабатывать, если нажата кнопка "Поиск фильма" и переводить в состояние
# ожидания выбора года
@search_router.message(StateFilter(GeneralConditions.first_choice))
async def process_select_year_command(message: Message, state: FSMContext):       # Нажатие на кнопку поиск фильма
    await message.answer(text=LEXICON["year"], reply_markup=years_films)
    # Устанавливаем состояние выбора года
    await state.set_state(GeneralConditions.select_year)


# Этот хэндлер будет срабатывать если выбран один из годов и переводить в состояние выбора жанра
@search_router.message(StateFilter(GeneralConditions.select_year))
async def process_select_genre_command(message: Message, state: FSMContext):
    await message.answer(text="genre", reply_markup=genre_films)
    # Устанавливаем состояние выбора жанра
    await state.set_state(GeneralConditions.select_genre)


# Этот хэндлер будет срабатывать если выбран один из жанров и переводить в состояние выбора рейтинга
@search_router.message(StateFilter(GeneralConditions.select_genre))
async def process_select_genre_command(state: FSMContext):
    pass
    # Устанавливаем состояние выбора рейтинга
    await state.set_state(GeneralConditions.select_rating)


# Этот хэндлер будет срабатывать если выбран рейтинг и переводить в состояние выбора времени просмотра
@search_router.message(StateFilter(GeneralConditions.select_rating))
async def process_select_time_command(state: FSMContext):
    pass
    # Устанавливаем состояние выбора времени просмотра
    await state.set_state(GeneralConditions.select_time)


# Этот хэндлер будет срабатывать если выбрано время просмотра и переводить в ???
@search_router.message(StateFilter(GeneralConditions.select_time))
async def process_select_review_command(state: FSMContext):
    pass
