from aiogram import Router
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery


from .states import GeneralConditions
from keyboards.keyboards import (
get_trailer_favorite_film,
main_builder
)
from config.config import MOVIES_JSON
from classes.film_favorites_picker import FavoritesFilms
from lexicon.lexicon import LEXICON


router = Router()
user = FavoritesFilms(MOVIES_JSON)


# Обрабатываем хэндлер случайного фильма из списка
@router.callback_query(GeneralConditions.favorite_film)
async def pick_favorite_movie(callback: CallbackQuery, state: FSMContext):
    data = callback.data
    if data == "favorite_next_film":
        # Получаем случайный фильм из списка избранных фильмов
        # Функция случайного выбора фильма из списка
        film = await user.processing_film_favorites(state=state)
        # Функция нахождения словаря фильма
        criteria_film = user.movie_favorites(film)
        # Сохраняем название последнего выданного фильма из списка лайков
        # Берем, название фильма (это надо для удаления из списка лайконых фильмов, если пользователь
        # нажмет клавишу убрать лайк)
        title_film = criteria_film['title']
        await state.update_data(the_last_movie=title_film)
        # Берем ссылку трейлера для клавиатуры
        trailer_film = criteria_film['trailer_url']
        # Функция красивого вывода фильма
        print_film = user.format_movie(criteria_film)
        # inline-клавиатура
        keyboard = get_trailer_favorite_film(trailer_film)
        # Выводим случайный фильм и inline-клавиатуру
        await callback.message.edit_text(text=print_film, reply_markup=keyboard, parse_mode="HTML")
        # Остаемся в том же состоянии
        await state.set_state(GeneralConditions.favorite_film)

    elif data == "favorite_dislike_film":
        # Функция удаления фильма из списка избранных фильмов
        await user.dislike_film(state=state)
        # Выводим сообщение о том, что у фильма убран лайк и отправляем пользователя в главное меню
        await callback.message.answer(text=LEXICON['dislike'], reply_markup=main_builder)
        # Переходим в состояние главного меню
        await state.set_state(GeneralConditions.first_choice)

    elif data == "favorite_main_menu":
        # Открываем кнопки главного меню и переводим в состояние первого выбора в главном меню
        await callback.message.answer(text=LEXICON["/go"], reply_markup=main_builder)
        # Указываем состояние "первого выбора"
        await state.set_state(GeneralConditions.first_choice)
    await callback.answer()


# Обрабатываем непонятные сообщения пользователя в состоянии случайного фильма из списка избранного
@router.message(GeneralConditions.random_film)
async def processing_of_incomprehensible_messages(message: Message):
    await message.answer(text=LEXICON['random_film'])
