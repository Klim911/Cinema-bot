from aiogram.fsm.state import State, StatesGroup, default_state


class GeneralConditions(StatesGroup):       # Общие состояния
    # Перечисляем возможные состояния главного меню
    first_choice = State()          # Состояние первого выбора в главном меню
    list_of_films = State()         # Состояние в кнопке "список фильмов"
    selected_films = State()        # Состояние в кнопке "избранные фильмы"
    select_year = State()           # Состояние ожидания выбора года
    select_genre = State()          # Состояние ожидания выбора жанра
    select_rating = State()         # Состояние ожидания выбора рейтинга
    select_time = State()           # Состояние ожидания выбора времени просмотра
    select_review = State()         # Состояние ожидания выбора обзора фильма
    select_sorting_rating = State() # Состояние ожидания выбора сортировки по рейтингу
    select_sorting_likes = State()  # Состояние ожидания выбора сортировки по лайкам
    showing_results = State()       # Показ результатов
    film_review = State()           # Состояние ожидания выбора обзора фильма
