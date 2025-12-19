import json
import aiofiles
from typing import List, Dict, Optional

from aiogram.fsm.context import FSMContext


class FilmDatabase:
    """База данных фильмов"""
    def __init__(self, json_file: str = "movies.json"):
        # Загружаем базу фильмов из JSON файла
        with open(json_file, "r", encoding="utf-8") as f:
            self.data = json.load(f)
        self.films_list = self.data["films"]

    def convert_year_callback(self, year_data: str) -> Optional[List[int]]:
        """Преобразуем callback_data годов в диапазон лет"""
        renge_of_years = {              # - диапазон лет
            "years_90": [1990, 1999],
            "years_2000": [2000, 2009],
            "years_2010": [2010, 2019],
            "years_2020": [2020, 2025],
            "year_pass": None           #Пропуск - любой год
        }
        return renge_of_years.get(year_data) if year_data else None

    def convert_genre_callback(self, genre_data: str) -> Optional[str]:
        """Преобразуем callback_data жанров в русские названия"""
        russian_names = {           # - русские названия
            "genre_comedy": "комедия",
            "genre_thriller": "триллер",
            "genre_detective": "детектив",
            "genre_drama": "драма",
            "genre_horror": "ужасы",
            "genre_adventure": "приключения",
            "genre_action": "боевик",
            "genre_pass": None    # Пропуск - любой жанр
        }
        return russian_names.get(genre_data) if genre_data else None

    def convert_rating_callback(self, rating_data: str) -> Optional[float]:
        """Преобразуем callback_data рейтинга в минимальное значение"""
        grade = {                   # - оценка
            "rating_high": 8.0,     # Высокий 8.0+
            "rating_good": 7.0,     # Хороший 7.0+
            "rating_average": 6.0,  # Средний 6.0+
            "rating_pass": None     # Пропуск - любой рейтинг
        }
        return grade.get(rating_data) if rating_data else None

    def convert_time_callback(self, time_data: str) -> Optional[int]:
        """Преобразуем callback_data времени в максимальную длительность"""
        max_time = {                # - максимальная длительность
            "time_short": 90,       # Короткий до 90 мин
            "time_average": 120,    # Средний до 120 мин
            "time_long": 150,       # Длинный до 150 мин
            "time_very_long": 999,  # Очень длинный
            "time_pass": None       # Пропуск - любое время
        }
        return max_time.get(time_data) if time_data else None

    def search_films(self,          # - поиск фильмов
                     year_callback: str = None,
                     genre_callback: str = None,
                     rating_callback: str = None,
                     time_callback: str = None) -> List[Dict]:
        """Ищем фильмы по выбранным критериям. Если callback будет pass - этот критерий будет игнорироваться"""
        filtered_films = self.films_list.copy()

        # Фильтр 1: по году (если не пропущен)
        decade = self.convert_year_callback(year_callback)
        if decade:
            filtered_films = [film for film in filtered_films if decade[0] <= int(film["years"]) <= decade[1]]

        # Филтр 2: по жанру (если не пропущен)
        genre = self.convert_genre_callback(genre_callback)
        if genre:
            filtered_films = [film for film in filtered_films if genre in film["genres"]]

        # Фильтр 3: по рейтингу (если не пропущен)
        min_rating = self.convert_rating_callback(rating_callback)
        if min_rating:
            filtered_films = [film for film in filtered_films if film["ratings"] >= min_rating]

        # Фильтр 4: по времени (если не пропущен)
        max_duration = self.convert_time_callback(time_callback)
        if max_duration:
            filtered_films = [film for film in filtered_films if film["duration"] <= max_duration]

        return filtered_films


"""
Модуль для преобразования callback_data в читаемые названия
"""

# Маппинг годов
year_mapping = {
    "years_90": "1990-1999",
    "years_2000": "2000-2009",
    "years_2010": "2010-2019",
    "years_2020": "2020-2025",
    "year_pass": "Любой год"
}

# Маппинг жанров
genre_mapping = {
    "genre_comedy": "Комедия",
    "genre_thriller": "Триллер",
    "genre_detective": "Детектив",
    "genre_drama": "Драма",
    "genre_horror": "Ужасы",
    "genre_adventure": "Приключения",
    "genre_action": "Боевик",
    "genre_pass": "Любой жанр"
}

# Маппинг рейтингов
rating_mapping = {
    "rating_high": "Высокий (8.0+)",
    "rating_good": "Хороший (7.0+)",
    "rating_average": "Средний (6.0+)",
    "rating_pass": "Любой рейтинг"
}

# Маппинг времени
time_mapping = {
    "time_short": "Короткий (до 90 мин)",
    "time_average": "Средний (до 120 мин)",
    "time_long": "Длинный (до 150 мин)",
    "time_very_long": "Очень длинный",
    "time_pass": "Любая длительность"
}


def get_readable_criteria(
        year_callback: str = None,
        genre_callback: str = None,
        rating_callback: str = None,
        time_callback: str = None
) -> dict:
    """
    Преобразует callback_data в читаемые названия

    Returns:
        dict: Словарь с читаемыми названиями критериев
    """
    return {
        "year": year_mapping.get(year_callback, "Любой год") if year_callback else "Любой год",
        "genre": genre_mapping.get(genre_callback, "Любой жанр") if genre_callback else "Любой жанр",
        "rating": rating_mapping.get(rating_callback, "Любой рейтинг") if rating_callback else "Любой рейтинг",
        "time": time_mapping.get(time_callback, "Любая длительность") if time_callback else "Любая длительность"
    }

def format_films_list(films: list, limit: int = 10) -> str:
    """Форматирует список фильмов в текст для сообщения"""
    films_text = "\n\n".join([
                    f"{i+1}. 🎬{film['title']}\n📅Год: {film['years']}\n"
                    f"⭐️Рейтинг: {film['ratings']}/10\n"
                    f"⏱️Длительность: {film['duration']}\n"
                    f"🎭Жанры: {', '.join(film['genres'])}"
                    for i, film in enumerate(films[:limit])
                ])
    return films_text


def sorting_selected_films_rating(data):
    sorted_films = sorted(data, key=lambda film: (-film["ratings"]))
    return sorted_films

def sorting_selected_films_years(data):
    sorted_films = sorted(data, key=lambda film: -int(film["years"]))
    return sorted_films

def sorting_selection_films_likes(data):
    sorted_films = sorted(data, key=lambda film: (-film["likes"]))
    return sorted_films


async def async_add_like_to_film(
        state: FSMContext,
        film_title: str,
        json_file_path: str = "movies.json",
):
    """
    Добавляет лайк фильму, если пользователь еще не лайкал его.

    Args:
        film_title: Название фильма
        user_id: ID пользователя
        json_file_path: Путь к файлу с фильмами
        likes_file_path: Путь к файлу с лайками пользователей

    Returns:
        int: Новое количество лайков
        None: Если фильм не найден или пользователь уже лайкал
    """

    # 1. Проверяем, лайкал ли пользователь уже этот фильм
    data = await state.get_data()
    list_favorites = data.get("favorites")
    if list_favorites is None:
        list_favorites = []

    film_title_lower = film_title.lower()

    for i in list_favorites:
        if i.lower() == film_title_lower.lower():
            return None

    # 2. Если пользователь не лайкал этот фильм, обновляем список в состоянии
    list_favorites.append(film_title)
    await state.update_data(favorites=list_favorites)

    # 3. Читаем данные о фильмах
    async with aiofiles.open(json_file_path, 'r', encoding='utf-8') as f:
        content = await f.read()
        data = json.loads(content)

    # 4. Ищем фильм и добавляем лайк
    film_found = False
    new_likes = 0

    for film in data["films"]:
        if film["title"].lower() == film_title_lower:
            film["likes"] = film.get("likes", 0) + 1
            new_likes = film["likes"]
            film_found = True
            break

    if not film_found:
        return None

    # 5. Сохраняем обновленные данные фильмов
    async with aiofiles.open(json_file_path, 'w', encoding='utf-8') as f:
        await f.write(json.dumps(data, ensure_ascii=False, indent=2))

    return new_likes