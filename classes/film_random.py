import json
from pathlib import Path
import random

from config.config import MOVIES_JSON
from classes.base_like_handler import BaseFilmLike


class RandomFilm(BaseFilmLike):

    def __init__(self, json_file=None):
        if json_file is None:
            self.json_file_path = MOVIES_JSON
        else:
            self.json_file_path = Path(json_file) if isinstance(json_file, str) else json_file
        # Загружаем базу фильмов из JSON файла
        with open(self.json_file_path, 'r', encoding='utf-8') as f:
            self.data = json.load(f)
        self.films_list = self.data["films"]

    def random_film(self):
        """Функция выбора случайного фильма"""
        film = random.choice(self.films_list)
        return film

    @staticmethod
    def format_film(film):
        """Красивый вывод фильма для пользователя"""
        text = (f"🎬 <b>{film['title']}</b>\n📅 Год: {film['years']}\n⭐ Рейтинг: {film['ratings']}\n"
                f"⏱️ Длительность: {film['duration']}\n🎭 Жанры: {', '.join(film['genres'])}\n────────────")
        if 'trailer_url' in film:
            response_text = f"{text}\n\n📹 <b>Трейлер доступен по ссылке ниже:</b>\n{film['trailer_url']}"
            return response_text
        else:
            response_text = f"{text}\n\n😔 <b>К сожалению, трейлер для этого фильма не найден</b>"
            return response_text
