from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.keyboard import ReplyKeyboardBuilder, InlineKeyboardBuilder
from lexicon.lexicon import LEXICON

# ----------Создаем клавиатуру главного меню----------
# Создаем кнопки главного меню
movie_search = KeyboardButton(text=LEXICON["movie_search"])
list_films = KeyboardButton(text=LEXICON["list_films"])
select_films = KeyboardButton(text=LEXICON["select_films"])
favorites_films = KeyboardButton(text=LEXICON['favorit_films'])
# Инициализируем билдер для клавиатуры главного меню
m_builder = ReplyKeyboardBuilder()
# Добавляем кнопки главного меню в билдер
# m_builder.row(movie_search, list_films, select_films, width=3)
# Создаем клавиатуру главного меню
main_builder = ReplyKeyboardMarkup(keyboard=[[movie_search], [list_films], [select_films], [favorites_films]],
    resize_keyboard=True, one_time_keyboard=True)

# ----------Создаем инлайн клавиатуры----------
# Создаем инлайн кнопки в разделе "год"
years_1 = InlineKeyboardButton(text="1990 - 1999", callback_data="years_90")
years_2 = InlineKeyboardButton(text="2000 - 2009", callback_data="years_2000")
years_3 = InlineKeyboardButton(text="2010 - 2019", callback_data="years_2010")
years_4 = InlineKeyboardButton(text="2020 - 2025", callback_data="years_2020")
pass_1 = InlineKeyboardButton(text="Пропуск", callback_data="year_pass")
back_1 = InlineKeyboardButton(text="Назад", callback_data="year_back")
# Создаем объект инлайн-клавиатуры связанный с годами фильма
years_films = InlineKeyboardMarkup(inline_keyboard=[[years_1], [years_2], [years_3], [years_4], [pass_1], [back_1]])

# Создаем инлайн кнопки в разделе "жанр"
comedy = InlineKeyboardButton(text="😁 comedy", callback_data="genre_comedy")
thriller = InlineKeyboardButton(text="😱 thriller", callback_data="genre_thriller")
detective = InlineKeyboardButton(text="🕵️ detective", callback_data="genre_detective")
drama = InlineKeyboardButton(text="🎭 drama", callback_data="genre_drama")
horror = InlineKeyboardButton(text="🧟 horror", callback_data="genre_horror")
adventure = InlineKeyboardButton(text="🎢 adventure", callback_data="genre_adventure")
action = InlineKeyboardButton(text="💥 action", callback_data="genre_action")
pass_2 = InlineKeyboardButton(text="Пропуск", callback_data="genre_pass")
back_2 = InlineKeyboardButton(text="Назад", callback_data="genre_back")
# Создаем объект инлайн-клавиатуры связанный с жанрами
genre_films = InlineKeyboardMarkup(inline_keyboard=[
    [comedy], [thriller], [detective], [drama], [horror], [adventure], [action], [pass_2], [back_2]
])

# Создаем инлайн кнопки в разделе "рейтинг"
high_8 = InlineKeyboardButton(text="Высокий 8.0+", callback_data="rating_high")
good = InlineKeyboardButton(text="Хороший 7.0+", callback_data="rating_good")
average = InlineKeyboardButton(text="Средний 6.0+", callback_data="rating_average")
pass_3 = InlineKeyboardButton(text="Пропуск", callback_data="rating_pass")
back_3 = InlineKeyboardButton(text="Назад", callback_data="rating_back")
# Создаем объект инлайн-клавиатуры связанный с рейтингом
rating_films = InlineKeyboardMarkup(inline_keyboard=[[high_8], [good], [average], [pass_3], [back_3]])

# Создаем инлайн кнопки в разделе "время просмотра"
short = InlineKeyboardButton(text="Короткий <9️⃣0️⃣ минут", callback_data="time_short")
t_average = InlineKeyboardButton(text="Средний 9️⃣0️⃣ ➖ 1️⃣2️⃣0️⃣ минут", callback_data="time_average")
long = InlineKeyboardButton(text="Длинный 2️⃣➖2️⃣.5️⃣ часа", callback_data="time_long")
very_long = InlineKeyboardButton(text="Очень длинный 3️⃣➕ часа", callback_data="time_very_long")
pass_4 = InlineKeyboardButton(text="Пропуск", callback_data="time_pass")
back_4 = InlineKeyboardButton(text="Назад", callback_data="time_back")
# Создаем объект инлайн-клавиатуры связанный с временем просмотра
time_films = InlineKeyboardMarkup(inline_keyboard=[[short], [t_average], [long], [very_long], [pass_4], [back_4]])

# Создаем инлайн кнопки в разделе "показ результатов", то есть когда появляется список по критериям
sort_rating = InlineKeyboardButton(text="Отсортировать по рейтингу ⭐️", callback_data="sorted_rating")
sort_year = InlineKeyboardButton(text="Отсортировать по году 📅", callback_data="sorted_year")
sort_like = InlineKeyboardButton(text="Отсортировать по лайкам 👍", callback_data="sorted_like")
review = InlineKeyboardButton(text="Трейлер фильма 👀", callback_data="review_film")
# Создаем объект инлайн-клавиатуры связанный с сортировкой
sort_films = InlineKeyboardMarkup(inline_keyboard=[[sort_rating], [sort_year], [sort_like], [review]])

# Создаем клавиатуру для просмотра трейлера
def get_trailer_keyboard(trailer_url: str | None = None) -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    if trailer_url:
        # URL-кнопка для открытия трейлера
        builder.button(text="🎬 Смотреть трейлер", url=trailer_url, callback_data="trailer")
        builder.button(text="🔙 Назад к списку", callback_data="back_list")
        builder.button(text="❤️ Поставить лайк", callback_data="like")
        builder.button(text="⚙️ Начать поиск заново", callback_data="main_menu")
    else:
        # Если трейлера нет
        builder.button(text="🔙 Назад к списку", callback_data="back_list")
        builder.button(text="❤️ Поставить лайк", callback_data="like")
        builder.button(text="⚙️ Начать поиск заново", callback_data="main_menu")
    builder.adjust(1)
    return builder.as_markup()

# Клавиатура только с кнопкой "назад к списку"
def get_back_to_list_keyboard() -> InlineKeyboardMarkup:
    back = InlineKeyboardButton(text="🔙 Назад к списку", callback_data="back_to_list")
    back_builder = InlineKeyboardMarkup(inline_keyboard=[[back]])
    return back_builder

# Создаем инлайн клавиатуру для раздела "Фильмы по рейтингу"
top_back = InlineKeyboardButton(text="⬅️ Предыдущая страница", callback_data="back_page")
top_continue = InlineKeyboardButton(text="Следующая страница ➡️", callback_data="continue_page")
top_choice = InlineKeyboardButton(text="🎬 Выбрать фильм", callback_data="choice_page")
main_menu = InlineKeyboardButton(text="📋 Вернуться в главное меню", callback_data="main_menu_page")
# Создаем объект инлайн-клавиатуры связанной с "топом фильмов по рейтингу"
top_ratings_films = InlineKeyboardMarkup(inline_keyboard=[[top_back], [top_choice], [top_continue], [main_menu]])

# Создаем инлайн кнопки для раздела "Случайный фильм из списка"
def get_trailer_random_film(trailer_url: str | None = None) -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    if trailer_url:
        # Если URL есть
        builder.button(text="⏭️🎬 Следующий фильм", callback_data="next_film")
        builder.button(text="❤️ Поставить лайк", callback_data="random_like_film")
        builder.button(text="🎬 Посмотреть трейлер", url=trailer_url, callback_data="random_trailer_film")
        builder.button(text="📋 Вернуться в главное меню", callback_data="random_main_menu")
    else:
        # Если трейлера нет
        builder.button(text="⏭️🎬 Следующий фильм", callback_data="next_film")
        builder.button(text="❤️ Поставить лайк", callback_data="random_like_film")
        builder.button(text="📋 Вернуться в главное меню", callback_data="random_main_menu")
    builder.adjust(1)
    return builder.as_markup()

# Создаем инлайн клавиатуру для раздела "Случайный фильм из избранного"
def get_trailer_favorite_film(trailer_url: str | None = None) -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    if trailer_url:
        # Если есть ссылка на трейлер
        builder.button(text="🎬 Посмотреть трейлер", url=trailer_url, callback_data="favorite_trailer_film")
        builder.button(text="⏭️🎬 Следующий фильм", callback_data="favorite_next_film")
        builder.button(text="💔 Убрать из списка избранного", callback_data="favorite_dislike_film")
        builder.button(text="📋 Вернуться в главное меню", callback_data="favorite_main_menu")
    else:
        # Если трейлера нет
        builder.button(text="⏭️🎬 Следующий фильм", callback_data="favorite_next_film")
        builder.button(text="💔 Убрать из списка избранного", callback_data="favorite_dislike_film")
        builder.button(text="📋 Вернуться в главное меню", callback_data="favorite_main_menu")
    builder.adjust(1)
    return builder.as_markup()
