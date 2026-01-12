from aiogram import Router
from aiogram.filters import StateFilter
from aiogram.types import Message, CallbackQuery

from .states import GeneralConditions
from config.config import MOVIES_JSON
from keyboards.keyboards import *
from classes.films_service_top import *


router = Router()
user = RatingsFilms(MOVIES_JSON)

# Обрабатываем хэндлер, кнопки списка фильмов по рейтингу
@router.callback_query(GeneralConditions.sorted_rating_list_films)
async def view_first_list(callback: CallbackQuery, state: FSMContext):    # Просмотр первого списка
    data = callback.data
    if data == "continue_page":
        # Достаем сохраненную страницу
        data1 = await state.get_data()
        page = data1.get("str_page")
        # Увеличиваем страницу на один и красиво выводим
        page += 1                              # Увеличиваем страницу на один
        films = user.get_current_page(page)     # Определяем список, для вывода
        if isinstance(films, list):
            # Сохраняем страницу пользователя
            await state.update_data(str_page=page)
        else:
            await callback.message.answer(text=LEXICON["continue_ratings_list"])
        page_print = user.format_page(films)    # Выводим страницу
        # Выводим список фильмов и inline-клавиатуры
        await callback.message.edit_text(text=page_print, reply_markup=top_ratings_films)
        # Остаемся в том же состоянии
        await state.set_state(GeneralConditions.sorted_rating_list_films)
    elif data == "choice_page":
        # Выводим сообщение, чтобы пользователь выбрал фильм из списка
        await callback.message.answer(text=LEXICON["review"])
        # Переводим в состояние просмотра трейлера
        await state.set_state(GeneralConditions.trailer_film)
    elif data == "back_page":
        # Достаем сохраненную страницу
        data1 = await state.get_data()
        page = data1.get("str_page")
        # Уменьшаем страницу на один и красиво выводим
        page -= 1               # Уменьшаем страницу на один
        films = user.get_current_page(page)  # Определяем список, для вывода
        if isinstance(films, list):
            # Сохраняем страницу пользователя
            await state.update_data(str_page=page)
        else:
            await callback.message.answer(text=LEXICON["back_ratings_list"])
        page_print = user.format_page(films)  # Выводим страницу
        # Выводим список фильмов и inline-клавиатуры
        await callback.message.edit_text(text=page_print, reply_markup=top_ratings_films)
        # Остаемся в том же состоянии
        await state.set_state(GeneralConditions.sorted_rating_list_films)
    elif data == "main_menu_page":
        # Открываем кнопки главного меню и переводим в состояние первого выбора в главном меню
        await callback.message.answer(text=LEXICON["/go"], reply_markup=main_builder)
        # Указываем состояние "первого выбора"
        await state.set_state(GeneralConditions.first_choice)

# Обрабатываем непонятные сообщения пользователя в состоянии первого показа списка фильмов по рейтингу
@router.message(StateFilter(GeneralConditions.sorted_rating_list_films))
async def processing_of_jambs(message: Message):
    await message.answer(text=LEXICON["no_ratings"])

# Этот хэндлер будет срабатывать, если пользователь захочет посмотреть трейлер из списка фильмов по рейтингу
# и будет вводить номер фильма из списка
@router.message(StateFilter(GeneralConditions.trailer_film))
async def process_film_number(message: Message, state: FSMContext):
    try:
        # Пробуем преобразовать текст в число
        film_number = int(message.text.strip())
        # Достаем сохраненную страницу
        data1 = await state.get_data()
        page = data1.get("str_page")
        # Получаем список наших фильмов
        films = user.get_current_page(page)
        # Сохраняем этот список, для возврата к нему из состояния просмотра трейлера
        await state.update_data(films_top=films)
        # Проходим проверку, чтобы число пользователя было номером фильма
        numbers = user.number_on_the_list(films)            # Тут создается список с номерами фильмов из списка
        if film_number in numbers:
            # Сохраняем номер выбранного фильма
            await state.update_data(film_number=film_number)
            result = user.beautiful_format_movie(films, film_number)             # Красивый вывод текста выбранного фильма
            keyboard = get_trailer_keyboard(user.trailer(films, film_number)) # Делаем переход на трейлер
            # Выводим описание фильма, и инлайн клавиатуру
            await message.answer(text=result, reply_markup=keyboard, parse_mode="HTML")
            # Устанавливаем состояние просмотра трейлера
            await state.set_state(GeneralConditions.top_trailer_film)
        else:
            await message.answer(text=LEXICON['no_number'])
            await state.set_state(GeneralConditions.trailer_film)
    except ValueError:
        # Пользователь ввел не число
        await message.answer(text="❌ Пожалуйста, введите номер фильма (только цифру).\n")

# Этот хендлер будет срабатывать, когда пользователю будет представлен фильм. Хэндлер обрабатывает кнопки:
# "назад к списку, лайк, просмотр трейлера, главное меню"
@router.callback_query(GeneralConditions.top_trailer_film)
async def processing_commands_in_trailer(callback: CallbackQuery, state: FSMContext):
    data_trailer = callback.data
    if data_trailer == "back_list":
        # Достаем из состояния список фильмов по рейтингу из которого он выбирал номер фильма
        user_films = await state.get_data()
        films = user_films.get("films_top")
        # Выводим список фильмов и просим снова выбрать номер фильма
        page_print = user.format_page(films)        # Красивый вывод страницы
        await callback.message.edit_text(text=page_print, reply_markup=top_ratings_films)
        # Переводим в состояние отсортированных фильмов по рейтингу
        await state.set_state(GeneralConditions.sorted_rating_list_films)

    elif data_trailer == "like":
        # Достаем из состояния номер и список фильмов для функции
        user_data = await state.get_data()
        user_number = user_data.get("film_number")          # Выбранный пользователем номер из списка
        user_list = user_data.get("films_top")              # Список фильмов с их номерами, который ранее выводил бот

        # Вызываем функцию, которая проставит лайк
        new_like = await user.add_like_to_film(sp=user_list, number=user_number, state=state)
        if new_like is not None:
            await callback.message.answer(
                text=f"{LEXICON['like']}{new_like} лайков\nНачните поиск заново",
                reply_markup=main_builder
            )
        else:
            await callback.message.answer(
                text=LEXICON["again_likes"],
                reply_markup=main_builder
            )

    elif data_trailer == "main_menu":
        # Открываем кнопки главного меню и переводим в состояние первого выбора в главном меню
        await callback.message.answer(text=LEXICON["/go"], reply_markup=main_builder)
        # Указываем состояние "первого выбора"
        await state.set_state(GeneralConditions.first_choice)
    await callback.answer()

# Обрабатываем непонятные сообщения пользователя в состоянии, когда пользователю будет представлен фильм
@router.message(GeneralConditions.top_trailer_film)
async def processing_messages(message: Message):
    await message.answer(text=LEXICON['random_film'])
