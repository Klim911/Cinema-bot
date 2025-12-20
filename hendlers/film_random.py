import json
import os
import random

from aiogram.fsm.context import FSMContext

current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
file_path = os.path.join(parent_dir, 'movies.json')

class RandomFilm:

    def __init__(self, json_file):
        # Загружаем базу фильмов из JSON файла
        full_path = json_file if os.path.isabs(json_file) else os.path.join(parent_dir, json_file)
        with open(full_path, 'r', encoding='utf-8') as f:
            self.data = json.load(f)
        self.films_list = self.data["films"]

    def random_film(self):
        """Функция выбора рандомного фильма"""
        film = random.choice(self.films_list)
        return film

    def format_film(self, film):
        """Красивый вывод фильма для пользователя"""
        text = (f"🎬 <b>{film['title']}</b>\n📅 Год: {film['years']}\n⭐ Рейтинг: {film['ratings']}\n"
                f"⏱️ Длительность: {film['duration']}\n🎭 Жанры: {', '.join(film['genres'])}\n────────────")
        return text


pr = RandomFilm("movies.json")
res = pr.random_film()
ser = pr.format_film(res)
print(ser)