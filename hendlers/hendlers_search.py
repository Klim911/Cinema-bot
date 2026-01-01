from aiogram import F, Router
from aiogram.filters import StateFilter
from aiogram.types import Message, CallbackQuery

from .states import GeneralConditions
from keyboards.keyboards import *
from .film_database import *
from .films_service_top import *
from .film_random import *
from .film_favorites_picker import FavoritesFilms




router = Router()
db = FilmDatabase("movies.json")

# Этот хэендлер будет срабатывать, если нажата кнопка "Поиск фильма" и переводить в состояние
# ожидания выбора года
@router.message(F.text.in_([LEXICON["movie_search"],
                           LEXICON["list_films"],
                           LEXICON["select_films"],
                            LEXICON["favorit_films"]]),
                                StateFilter(GeneralConditions.first_choice))
async def handle_main_menu(message: Message, state: FSMContext):
    if message.text == LEXICON["movie_search"]:     # Нажатие на кнопку поиск фильма
        # Выводим сообщение выбора года и инлайн клавиатуру
        await message.answer(text=LEXICON["year"], reply_markup=years_films)
        # Устанавливаем состояние выбора года
        await state.set_state(GeneralConditions.select_year)
    elif message.text == LEXICON["list_films"]:
        user = RatingsFilms("movies.json")
        # Страница по умолчанию
        page = 0
        # Делаем и выводим первую страницу фильмов по рейтингу
        f = user.get_current_page(page)  # Первая страница
        if f:
            # Сохраняем страницу по умолчанию
            await state.update_data(str_page=page)
        print_user = user.format_page(f)  # Вывод первой страницы
        await message.answer(text=print_user, reply_markup=top_ratings_films)
        # Устанавливаем состояние Фильмов по рейтингу
        await state.set_state(GeneralConditions.sorted_rating_list_films)
    elif message.text == LEXICON["select_films"]:
        user = RandomFilm("movies.json")
        # Делаем и выводим рандомный фильма
        film = user.random_film()               # Выбирается рандомный фильм
        if film:
            # Сохраняем фильм в состояние
            await state.update_data(random_film=film)
        trailer_film = film['trailer_url']      # Берем ссылку трейлера для клавиатуры
        print_film = user.format_film(film)     # Красивый вывод фильма
        keyboard = get_trailer_random_film(trailer_film)
        await message.answer(text=print_film, reply_markup=keyboard, parse_mode="HTML")
        # Устанавливаем состояние Рандомного фильма
        await state.set_state(GeneralConditions.random_film)
    elif message.text == LEXICON["favorit_films"]:
        # # Достаем из FSM наш список с избранными фильмами
        # data = await state.get_data()
        # films = data.get("favorites")
        # if films is not None:
            # Получаем случайный фильм из списка избранных фильмов
        user = FavoritesFilms("movies.json")
        film = await user.processing_film_favorites(state=state)    # Функция случайного выбора фильма из списка
        if film is not None:
            criteria_film = user.movie_favorites(film)              # Функция нахождения словаря фильма
            trailer_film = criteria_film['trailer_url']             # Берем ссылку трейлера для клавиатуры
            print_film = user.format_movie(criteria_film)           # Функция красивого вывода фильма
            keyboard = get_trailer_favorite_film(trailer_film)      # Инлайн клавиатура
            # Выводим случайный фильм и инлайн клавиатуру
            await message.answer(text=print_film, reply_markup=keyboard, parse_mode="HTML")
            # Устанавливаем состояние фильма из списка избранных фильмов
            await state.set_state(GeneralConditions.favorite_film)
        else:
            await message.answer(text=LEXICON["random_favorites_film"])

# Обрабатываем непонятные сообщения пользователя в состоянии ожидания первого выбора
@router.message(StateFilter(GeneralConditions.first_choice))
async def process_unknown_input_in_showing_state(message: Message):
    await message.answer(text=LEXICON["main"], reply_markup=main_builder)


# Этот хэндлер будет срабатывать если выбран один из годов и переводить в состояние выбора жанра
@router.callback_query(StateFilter(GeneralConditions.select_year))
async def process_select_genre_command(callback: CallbackQuery, state: FSMContext):
    # Получаем данные из callback_data и обрабатываем варианты
    year_data = callback.data
    if year_data in {"years_90", "years_2000", "years_2010", "years_2020", "year_pass"}:
        # Сохраняем выбранный год
        await state.update_data(year=year_data)
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

# Этот хендлер будет срабатывать если выбран жанр фильма и переводить в состояние выбора рейтинга
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
        await callback.message.edit_text(text=LEXICON["year"], reply_markup=years_films)
        await state.set_state(GeneralConditions.select_year)
    await callback.answer()

# Обрабатываем непонятные сообщения пользователя в состоянии выбора года
@router.message(StateFilter(GeneralConditions.select_genre))
async def process_unknown_input_in_genre_state(message: Message):
    await message.answer(text=LEXICON["no_genre"], reply_markup=genre_films)

# Этот хэндлер будет срабатывать если выбран рейтинг и переводить в состояние выбора времени просмотра
@router.callback_query(StateFilter(GeneralConditions.select_rating))
async def process_select_time_command(callback: CallbackQuery, state: FSMContext):
    # Получаем данные из callback_data и обрабатываем варианты
    rating_data = callback.data
    if rating_data in {"rating_high", "rating_good", "rating_average", "rating_pass"}:
        # Сохраняем выбранный жанр
        await state.update_data(rating=rating_data)
        # Переходим к следующему шагу - выбору времени просмотра
        await callback.message.edit_text(text=LEXICON["time"], reply_markup=time_films)
        # Устанавливаем состояние выбора времени просмотра
        await state.set_state(GeneralConditions.select_time)
    elif rating_data == "rating_back":
        # Кнопка "Назад". Устанавливаем состояние выбора жанра и появление кнопок выбора жанра
        await callback.message.edit_text(text=LEXICON["genre"], reply_markup=genre_films)
        await state.set_state(GeneralConditions.select_genre)
    await callback.answer()

# Обрабатываем непонятные сообщения пользователя в состоянии выбора рейтинга
@router.message(GeneralConditions.select_rating)
async def process_unknown_input_in_rating_state(message: Message):
    await message.answer(text=LEXICON["no_rating"], reply_markup=rating_films)


# Этот хэндлер будет срабатывать если выбрано время просмотра и переводить в состояние "показ результатов"
@router.callback_query(StateFilter(GeneralConditions.select_time))
async def process_select_time_command(callback: CallbackQuery, state: FSMContext): # Команда выбора процесса времени
    # Получаем данные из callback_data и обрабатываем варианты
    time_data = callback.data
    if time_data in {"time_short", "time_average", "time_long", "time_very_long", "time_pass"}:
        # Сохраняем выбранный жанр
        await state.update_data(time=time_data)

        # Получаем все выборы пользователя
        user_choices = await state.get_data()
        separator = "<code>────────────────────────────────</code>"

        # Получаем читаемые названия
        readable = get_readable_criteria(
            year_callback=user_choices.get("year"),
            genre_callback=user_choices.get("genre"),
            rating_callback=user_choices.get("rating"),
            time_callback=time_data
        )
        # Ищем фильмы по всем критериям
        results = db.search_films(
            year_callback=user_choices.get("year"),
            genre_callback=user_choices.get("genre"),
            rating_callback=user_choices.get("rating"),
            time_callback=time_data
        )
        # Сохраняем результат списка фильмов, выбранные пользователем по его критериям
        await state.update_data(current_films=results,
                                search_criteria={
                                    "year": user_choices.get("year"),
                                    "genre": user_choices.get("genre"),
                                    "rating": user_choices.get("rating"),
                                    "time": time_data
                                })

        # print(results)
        if results:
            kriter = (f"<b>Ваши критерии: </b>\n"
                          f"📅Год: {readable["year"]}\n"
                          f"🎭Жанр: {readable["genre"]}\n"
                          f"⭐️Рейтинг: {readable["rating"]}\n"
                          f"Время: {readable["time"]}\n"
                          f"{separator}")

            films_text = db.format_movie(results)
            # print(films_text)
            await callback.message.edit_text(
                text=f"{kriter}\n<b>Список фильмов по вашим критериям: </b>\n{films_text}",
                reply_markup=sort_films
            )
            # Сохраняем список фильмов
            await state.update_data(films=films_text)
            # Устанавливаем состояние показа результатов
            await state.set_state(GeneralConditions.showing_results)
        else:
            await callback.message.edit_text(text=LEXICON["no_results"], reply_markup=main_builder)
            # Устанавливаем состояние первого выбора, откроются кнопки главного меню
            await state.set_state(GeneralConditions.first_choice)
    elif time_data == "time_back":
        # Кнопка "Назад". Устанавливаем состояние выбора рейтинга и появление кнопок выбора рейтинга
        await callback.message.edit_text(text=LEXICON["rating"], reply_markup=rating_films)
        # Устанавливаем состояние выбора рейтинга
        await state.set_state(GeneralConditions.select_rating)
    await callback.answer()

# Обрабатываем непонятные сообщения пользователя в состоянии выбора времени просмотра
@router.message(StateFilter(GeneralConditions.select_time))
async def process_unknown_input_in_time_state(message: Message):
    await message.answer(text=LEXICON["no_time"], reply_markup=time_films)

# Этот хэндлер будет срабатывать когда будет виден список рекомендаций и когда пользователь захочет отсортировать
# список
@router.callback_query(StateFilter(GeneralConditions.showing_results))
async def process_sorting_selection(callback: CallbackQuery, state: FSMContext): # Обработать выбор сортировки
    # Получаем данные из callback_data и обрабатываем варианты
    sort_data = callback.data
    user_data = await state.get_data()
    if sort_data == "sorted_rating":
        # Берем сохраненные фильмы
        films = user_data.get("current_films")
        list_films1 = db.sorting_selected_films_rating(films.copy()) # Сортируем по рейтингам
        # Обновляем результат отсортированного списка фильмов, для дальнейшего поиска по номерам
        await state.update_data(current_films=list_films1)
        films_text = db.format_movie(list_films1) # Делаем красивый вывод
        # Обновляем список фильмов
        await state.update_data(films=films_text)
        # Выводим отсортированный список по рейтингу
        await callback.message.answer(text=films_text, reply_markup=sort_films)
        # Остаемся в том же состоянии
        await state.set_state(GeneralConditions.showing_results)
    elif sort_data == "sorted_year":
        # Берем сохраненные фильмы
        films = user_data.get("current_films")
        list_films2 = db.sorting_selected_films_years(films.copy()) # Сортируем по годам
        # Обновляем результат отсортированного списка фильмов, для дальнейшего поиска по номерам
        await state.update_data(current_films=list_films2)
        films_text = db.format_movie(list_films2) # Делаем красивый вывод
        # Обновляем список фильмов
        await state.update_data(films=films_text)
        # Выводим отсортированный список по году
        await callback.message.answer(text=films_text, reply_markup=sort_films)
        # Остаемся в том же состоянии
        await state.set_state(GeneralConditions.showing_results)
    elif sort_data == "sorted_like":
        films = user_data.get("current_films")
        list_films3 = db.sorting_selection_films_likes(films.copy()) # Сортируем по лайкам
        # Обновляем результат отсортированного списка фильмов, для дальнейшего поиска по номерам
        await state.update_data(current_films=list_films3)
        films_text = db.format_movie(list_films3) # Делаем красивый вывод
        # Обновляем список фильмов
        await state.update_data(films=films_text)
        # Выводим отсортированный список по лайкам
        await callback.message.answer(text=films_text, reply_markup=sort_films)
        # Остаемся в том же состоянии
        await state.set_state(GeneralConditions.showing_results)
    elif sort_data == "review_film":
        # Просим ввести номер по списку для трейлера
        await callback.message.answer(text=LEXICON["review"])
        # Устанавливаем состояние выбора номера обзора фильма
        await state.set_state(GeneralConditions.film_review)
    elif sort_data == "sort_main_menu":
        # Открываем кнопки главного меню и переводим в состояние первого выбора в главном меню
        await callback.message.answer(text=LEXICON["/go"], reply_markup=main_builder)
        # Указываем состояние "первого выбора"
        await state.set_state(GeneralConditions.first_choice)
    await callback.answer()

# Обрабатываем непонятные сообщения пользователя в состоянии показа результатов
@router.message(StateFilter(GeneralConditions.showing_results))
async def process_unknown_input_in_showing_state(message: Message):
    await message.answer(text=LEXICON["no_show"], reply_markup=sort_films)  #?

# Этот хэндлер будет срабатывать, когда пользователь введет номер фильма, чтобы посмотреть его трейлер.
@router.message(StateFilter(GeneralConditions.film_review))
async def process_film_number(message: Message, state: FSMContext):
    try:
        # Пробуем преобразовать текст в число
        film_number = int(message.text.strip())
        # Получаем сохраненные фильмы из состояния
        user_data = await state.get_data()
        films = user_data.get("current_films", [])
        # Проверяем, что номер в допустимом диапазоне
        if 1 <= film_number <= len(films):
            # Получаем выбранный фильм (индекс на 1 меньше номера)
            selected_film = films[film_number - 1]
            # Получаем URL трейлера из данных фильма
            trailer_url = selected_film.get("trailer_url")
            # Формируем информацию о фильме
            film_info = (
                f"🎬 {selected_film['title']}\n"
                f"📅 Год: {selected_film['years']}\n"
                f"⭐ Рейтинг: {selected_film['ratings']}/10\n"
                f"⏱️ Длительность: {selected_film['duration']} мин\n"
                f"🎭 Жанры: {', '.join(selected_film['genres'])}\n"
                f"────────────"
            )
            if trailer_url:
                # Кнопка для открытия трейлера (URL-кнопка)
                response_text = (f"{film_info}\n\n📹 <b>Трейлер доступен по ссылке ниже:</b>"
                                 f"{selected_film['trailer_url']}")
            else:
                # Если трейлера нет в базе
                response_text = f"{film_info}\n\n😔 <b>К сожалению, трейлер для этого фильма не найден</b>"
            keyboard = get_trailer_keyboard(trailer_url)
            # Кнопки для навигации

            await message.answer(
                text=response_text,
                reply_markup=keyboard,
                parse_mode="HTML"
            )
            await state.update_data(selected_film=selected_film)
            # Сохраняем состояние просмотра трейлера
            await state.set_state(GeneralConditions.film_trailer)
        else:
            # Номер вне диапазона
            await message.answer(text=f"❌ Номер должен быть от 1 до {len(films)}.\n"
                     f"Пожалуйста, введите номер фильма из списка:")

    except ValueError:
        # Пользователь ввел не число
        await message.answer(text="❌ Пожалуйста, введите номер фильма (только цифру).\n"
                 f"Например: 1, 2, 3 и т.д.")

# Этот хэндлер будет срабатывать, когда пользователь нажмет на просмотр трейлера, обработаем нажатие на лайк и назад,
# а также возможность начать новый поиск
@router.callback_query(StateFilter(GeneralConditions.film_trailer))
async def processing_commands_in_trailer(callback: CallbackQuery, state: FSMContext):
    trailer_data = callback.data
    if trailer_data == "back_list":
        # Получаем выбранный результат списка фильмов, выбранные пользователем по его критериям
        data = await state.get_data()
        user_current_films = data.get("films")
        # Выводим список фильмов и просим снова выбрать обзор какого смотреть
        await callback.message.edit_text(text=user_current_films, reply_markup=sort_films)
        # Переводим в состояние выбора из списка рекомендаций
        await state.set_state(GeneralConditions.showing_results)

    elif trailer_data == "like":
        # Получаем выбранный результат списка фильмов, выбранные пользователем по его критериям
        data = await state.get_data()
        user_choice = data.get("selected_film")
        film_title = user_choice['title']
        new_like = await async_add_like_to_film(state=state, film_title=film_title)
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
        await state.update_data()
    elif trailer_data == "main_menu":
        # Открываем кнопки главного меню и переводим в состояние первого выбора в главном меню
        await callback.message.answer(text=LEXICON["/go"], reply_markup=main_builder)
        # Указываем состояние "первого выбора"
        await state.set_state(GeneralConditions.first_choice)
    await callback.answer()
