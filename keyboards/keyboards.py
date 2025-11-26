from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton
from lexicon.lexicon import LEXICON

# ----------Создаем клавиатуру главного меню----------
# Создаем кнопки главного меню
movie_search = KeyboardButton(text=LEXICON["movie_search"])
list_films = KeyboardButton(text=LEXICON["list_films"])
select_films = KeyboardButton(text=LEXICON["select_films"])
# Инициализируем билдер для клавиатуры главного меню
m_builder = ReplyKeyboardMarkup
# Добавляем кнопки главного меню в билдер
m_builder.row(movie_search, list_films, select_films, width=3)
# Создаем клавиатуру главного меню
main_builder: ReplyKeyboardMarkup = m_builder.as_markup(
    one_time_keyboard=True, resize_keyboard=True
)

# ----------Создаем инлайн клавиатуры----------
# Создаем инлайн кнопки в разделе год
years_1 = InlineKeyboardButton(
    text="1990 - 1999", callback_data="years_90"
)
years_2 = InlineKeyboardButton(
    text="2000 - 2009", callback_data="years_2000"
)
years_3 = InlineKeyboardButton(
    text="2010 - 2019", callback_data="years_2010"
)
years_4 = InlineKeyboardButton(
    text="2020 - 2025", callback_data="years_2020"
)
pass_1 = InlineKeyboardButton(
    text="Пропуск", callback_data="year_pass"
)
back_1 = InlineKeyboardButton(
    text="Назад", callback_data="year_back"
)
# Создаем объект инлайн-клавиатуры связанный с годами фильма
years_films = InlineKeyboardMarkup(inline_keyboard=[[years_1], [years_2], [years_3], [years_4], [pass_1], [back_1]])

# Создаем инлайн кнопки в разделе жанр
comedy = InlineKeyboardButton(
    text="😁 comedy", callback_data="genre_comedy"
)
thriller = InlineKeyboardButton(
    text="😱 thriller", callback_data="genre_thriller"
)
detective = InlineKeyboardButton(
    text="🕵️ detective", callback_data="genre_detective"
)
drama = InlineKeyboardButton(
    text="🕵️ detective", callback_data="genre_detective"
)
horror = InlineKeyboardButton(
    text="🧟 horror", callback_data="genre_horror"
)
adventure = InlineKeyboardButton(
    text="🎢 adventure", callback_data="genre_adventure"
)
action = InlineKeyboardButton(
    text="💥 action", callback_data="genre_action"
)
pass_2 = InlineKeyboardButton(
    text="Пропуск", callback_data="genre_pass"
)
back_1 = InlineKeyboardButton(
    text="Назад", callback_data="genre_back"
)
# Создаем объект инлайн-клавиатуры связанный с жанрами
genre_films = InlineKeyboardMarkup(inline_keyboard=[
    [comedy], [thriller], [detective], [drama], [horror], [adventure], [action], [pass_2], [back_1]
])