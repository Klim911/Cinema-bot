import json
from typing import List, Dict, Optional


class FilmDatabase:
    """База данных фильмов"""
    def __init__(self, json_file: str = "movies.json"):
        # Загружаем базу фильмов из JSON файла
        with open(json_file, "r", encoding="utf-8") as f:
            self.data = json.load(f)

    def convert_year_callback(self, year_data: str) -> Optional[str]:
        """Преобразуем callback_data годов в диапазон лет"""
        renge_of_years = {              # - диапазон лет
            "years_90": "1990 - 1999",
            "years_2000": "2000 - 2009",
            "years_2010": "2010 - 2019",
            "years_2020": "years_2010",
            "year_pass": None           #Пропуск - любой год
        }
        return renge_of_years.get(year_data)

    def convert_genre_callback(self, genre_data: str) -> Optional[float]:
        """Преобразуем callback_data жанров в русские названия"""
        russian_names = {           # - русские названия
            "genre_comedy": "комедия",
            "genre_thriller": "триллер",
            "genre_detective": "детектив",
            "genre_drama": "драма",
            "genre_horror": "ужасы",
            "genre_adventure": "приключения",
            "genre_action": "боевик",
            "genre_pass": "None"    # Пропуск - любой жанр
        }
        return russian_names.get(genre_data)

    def convert_rating_callback(self, rating_data: str) -> Optional[str]:
        """Преобразуем callback_data рейтинга в минимальное значение"""
        grade = {                   # - оценка
            "rating_high": 8.0,     # Высокий 8.0+
            "rating_good": 7.0,     # Хороший 7.0+
            "rating_average": 6.0,  # Средний 6.0+
            "rating_pass": None     # Пропуск - любой рейтинг
        }
        return grade.get(rating_data)

    def convert_time_callback(self, time_data: str) -> Optional[int]:
        """Преобразуем callback_data времени в максимальную длительность"""
        max_time = {                # - максимальная длительность
            "time_short": 90,       # Короткий до 90 мин
            "time_average": 120,    # Средний до 120 мин
            "time_long": 150,       # Длинный до 150 мин
            "time_very_long": 999,  # Очень длинный
            "time_pass": None       # Пропуск - любое время
        }
        return max_time.get(time_data)
