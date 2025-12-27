import random
import os
import json

from aiogram.fsm.context import FSMContext

current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
file_path = os.path.join(parent_dir, 'movies.json')


class FavoritesFilms:
    def __init__(self, json_file):
        # Загружаем базу фильмов из JSON файла
        full_path = json_file if os.path.isabs(json_file) else os.path.join(parent_dir, json_file)
        with open(full_path, 'r', encoding='utf-8') as f:
            self.data = json.load(f)
        self.films_list = self.data["films"]


    async def processing_film_favorites(self, state):
        """Функция, которая достает случайный фильм из списка избранных"""
        # Достаем из FSM наш список с избранными фильмами
        data = await state.get_data()
        films = data.get("favorites")
        if len(films) != 0:
            random_film = random.choice(films)
            return random_film
        else:
            return None
        # if len(data) > 0:
        #     random_film = random.choice(data)
        #     return random_film
        # else:
        #     return None

    def movie_favorites(self, data):
        """Находим наш случайный фильм в нашем общем списке, и достаем словарь"""
        filme = None
        for i in self.films_list:
            for j, d in i.items():
                if d == data:
                    filme = i
                    break

        return filme

    def format_movie(self, data):
        """Красиво выводим фильм"""
        text = (f"🎬 <b>{data['title']}</b>\n📅 Год: {data['years']}\n⭐ Рейтинг: {data['ratings']}\n"
                f"⏱️ Длительность: {data['duration']}\n🎭 Жанры: {', '.join(data['genres'])}\n────────────")
        if 'trailer_url' in data:
            response_text = f"{text}\n\n📹 <b>Трейлер доступен по ссылке ниже:</b>\n{data['trailer_url']}"
            return response_text
        else:
            response_text = f"{text}\n\n😔 <b>К сожалению, трейлер для этого фильма не найден</b>"
            return response_text



# sp = ["Лофт", "300 спартанцев"]
# user = FavoritesFilms("movies.json")
# f = user.processing_film_favorites(sp)
# print(f)
# r = user.movie_favorites(f)
# print(r)
# re = user.format_movie(r)
# print(re)