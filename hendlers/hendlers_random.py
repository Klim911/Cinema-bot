from aiogram import Router
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext

from .states import GeneralConditions
from keyboards.keyboards import (
get_trailer_random_film,
main_builder
)
from config.config import MOVIES_JSON
from classes.film_random import RandomFilm
from lexicon.lexicon import LEXICON



router = Router()
user = RandomFilm(MOVIES_JSON)

# Обрабатываем хэндлер случайного фильма
@router.callback_query(GeneralConditions.random_film)
async def pick_random_movie(callback: CallbackQuery, state: FSMContext):
    data = callback.data
    if data == "next_film":
        # Получаем случайный фильм
        film  = user.random_film()
        # Сохраняем фильм в состояние FMS если нам надо будет его лайкать
        await state.update_data(random_film=film)
        # Ссылка на трейлер
        trailer_url = film['trailer_url']
        keyboard = get_trailer_random_film(trailer_url)
        # Красиво выводим
        print_film = user.format_film(film)
        # Выводим фильм и остаемся в том же состоянии
        await callback.message.edit_text(text=print_film, reply_markup=keyboard, parse_mode="HTML")
        await state.set_state(GeneralConditions.random_film)

    elif data == "random_like_film":
        # Вызываем функцию, которая проставит лайк
        new_like = await user.add_like_random_film(state=state)
        if new_like is not None:
            await callback.message.answer(
                text=f"{LEXICON['like']}{new_like} лайков.\n\nВозвращаемся в главное меню",
                reply_markup=main_builder
            )
            await state.set_state(GeneralConditions.first_choice)
        else:
            await callback.message.answer(
                text=f"{LEXICON["again_likes"]}\n\nВозвращаемся в главное меню",
                reply_markup=main_builder
            )
            await state.set_state(GeneralConditions.first_choice)

    elif data == "random_main_menu":
        # Открываем кнопки главного меню и переводим в состояние первого выбора в главном меню
        await callback.message.answer(text=LEXICON["/go"], reply_markup=main_builder)
        # Указываем состояние "первого выбора"
        await state.set_state(GeneralConditions.first_choice)
    await callback.answer()

# Обрабатываем непонятные сообщения пользователя в состоянии случайного фильма
@router.message(GeneralConditions.random_film)
async def processing_of_incomprehensible_messages(message: Message):
    await message.answer(text=LEXICON['random_film'])