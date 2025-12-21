from aiogram import Router
from aiogram.filters import StateFilter
from aiogram.types import Message, CallbackQuery

from .states import GeneralConditions
from keyboards.keyboards import *
from .film_random import *



router = Router()
user = RandomFilm("movies.json")

# Обрабатываем хэндлер рандомного фильма
@router.callback_query(GeneralConditions.random_film)
async def pick_random_movie(callback: CallbackQuery, state: FSMContext):
    data = callback.data
    if data == "next_film":
        # Получаем случайный фильм
        film  = user.random_film()
        # Сохраняем фильм в состояние FMS если нам надо будет его лайкать
        await state.update_data(random_fil=film)
        trailer_url = film['trailer_url']               # Ссылка на трейлер
        keyboard = get_trailer_random_film(trailer_url)
        print_film = user.format_film(film)             # Красиво выводим
        # Выводим фильм и остаемся в том же состоянии
        await callback.message.edit_text(text=print_film, reply_markup=keyboard, parse_mode="HTML")
        await state.set_state(GeneralConditions.random_film)

    elif data == "random_like_film":
        # Вызываем функцию, которая проставит лайк
        new_like = await user.add_like_random_film(state=state)
        if new_like is not None:
            await callback.message.answer(
                text=f"{LEXICON['like']}{new_like} лайков",
                reply_markup=main_builder
            )
        else:
            await callback.message.answer(
                text=LEXICON["again_likes"],
                reply_markup=main_builder
            )

    elif data == "random_main_menu":
        # Открываем кнопки главного меню и переводим в состояние первого выбора в главном меню
        await callback.message.answer(text=LEXICON["/go"], reply_markup=main_builder)
        # Указываем состояние "первого выбора"
        await state.set_state(GeneralConditions.first_choice)
    await callback.answer()