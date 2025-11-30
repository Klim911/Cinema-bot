from aiogram import F, Router, types
from aiogram.filters import StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup, default_state
from aiogram.types import Message, ContentType, CallbackQuery

from .states import GeneralConditions
from lexicon.lexicon import LEXICON
from keyboards.keyboards import *



router = Router()

# Этот хэендлер будет срабатывать, если нажата кнопка "Поиск фильма" и переводить в состояние
# ожидания выбора года
@router.message(StateFilter(GeneralConditions.first_choice))
async def process_select_year_command(message: Message, state: FSMContext):       # Нажатие на кнопку поиск фильма
    await message.answer(text=LEXICON["year"], reply_markup=years_films)
    # Устанавливаем состояние выбора года
    await state.set_state(GeneralConditions.select_year)


# Этот хэндлер будет срабатывать если выбран один из годов и переводить в состояние выбора жанра
@router.callback_query(StateFilter(GeneralConditions.select_year))
async def process_select_genre_command(callback: CallbackQuery, state: FSMContext):
    # Получаем данные из callback_data и обрабатываем варианты
    year_data = callback.data
    if year_data in {"years_90", "years_2000", "years_2010", "years_2020", "year_pass"}:
        # Сохраняем выбранный год
        await state.update_data(yaear=year_data)
        # Переходим к следующему шагу - выбор жанра
        await callback.message.edit_text(text=LEXICON["genre"], reply_markup=genre_films)
        # Устанавливаем состояние выбора жанра
        await state.set_state(GeneralConditions.select_genre)
    elif year_data == "year_back":
        # Устанавливаем состояние главного меню и появление кнопок главного меню
        await callback.message.delete() # Удаляем инлайн клавиатуру
        await callback.message.answer(text=LEXICON["/go"], reply_markup=main_builder)
        await state.set_state(GeneralConditions.first_choice)
    await callback.answer()

# Обрабатываем непонятные сообщения пользователя в состоянии выбора года
@router.message(StateFilter(GeneralConditions.select_year))
async def process_unknown_input_in_year_state(message: Message):
    await message.answer(text=LEXICON["no_years"], reply_markup=years_films)


@router.callback_query(StateFilter(GeneralConditions.select_genre))
async def process_select_rating_command(callback: CallbackQuery, state: FSMContext):
    # Получаем данные из callback_data и обрабатываем варианты
    genre_data = callback.data
    if genre_data in {"genre_comedy", "genre_thriller", "genre_detective", "genre_drama", "genre_horror",
                      "genre_adventure", "genre_action", "genre_pass"}:
        # Сохраняем выбранный жанр
        await state.update_data(genre=genre_data)
        # Переходим к следующему шагу - выбору рейтинга
        await callback.message.edit_text(text=LEXICON["rating"], reply_markup=rating_films)
        # Устанавливаем состояние выбора рейтинга
        await state.set_state(GeneralConditions.select_rating)
    elif genre_data == "genre_back":
        # Кнопка "Назад". Устанавливаем состояние выбора года и появление кнопок выбора года
        # await callback.message.delete()  # Удаляем инлайн клавиатуру
        await callback.message.edit_text(text=LEXICON["year"], reply_markup=years_films)
        await state.set_state(GeneralConditions.select_year)
    await callback.answer()

# Обрабатываем непонятные сообщения пользователя в состоянии выбора года
@router.message(StateFilter(GeneralConditions.select_genre))
async def process_unknown_input_in_genre_state(message: Message):
    await message.answer(text=LEXICON["no_genre"], reply_markup=genre_films)

# Этот хэндлер будет срабатывать если выбран рейтинг и переводить в состояние выбора времени просмотра
@router.message(StateFilter(GeneralConditions.select_rating))
async def process_select_time_command(message: Message, state: FSMContext):
    await message.answer(text=LEXICON["time"], reply_markup=time_films)
    # Устанавливаем состояние выбора времени просмотра
    await state.set_state(GeneralConditions.select_time)


# # Этот хэндлер будет срабатывать если выбрано время просмотра и переводить в ???
# @search_router.message(StateFilter(GeneralConditions.select_time))
# async def process_select_review_command(state: FSMContext):
#     pass
