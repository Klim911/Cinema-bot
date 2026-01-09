import random
import os
import json
import aiofiles


class FavoritesFilms:

    def __init__(self, json_file):
        current_dir = os.path.dirname(os.path.abspath(__file__))
        self.parent_dir = os.path.dirname(current_dir)
        if os.path.isabs(json_file):
            self.json_file_path = json_file
        else:
            self.json_file_path = os.path.join(self.parent_dir, json_file)
        # Загружаем базу фильмов из JSON файла
        with open(self.json_file_path, 'r', encoding='utf-8') as f:
            self.data = json.load(f)
        self.films_list = self.data["films"]

    @staticmethod
    async def processing_film_favorites(state):
        """Функция, которая достает случайный фильм из списка избранных"""
        # Достаем из FSM наш список с избранными фильмами
        data = await state.get_data()
        films = data.get("favorites")
        if len(films) != 0:
            random_film = random.choice(films)
            return random_film
        else:
            return None

    def movie_favorites(self, data):
        """Находим наш случайный фильм в нашем общем списке, и достаем словарь"""
        for i in self.films_list:
            for j, d in i.items():
                if d == data:
                    filme = i
                    return filme

    async def dislike_film(self, state):
        """Функция для удаления фильма из списка лайкнутых фильмов"""
        # 1. Удаляем фильм из списка лайкнутых фильмов
        # Достаем, из FSM наш список с избранными фильмами
        data = await state.get_data()
        movie = data.get("the_last_movie")
        # Достаем список лайкнутых фильмов
        films = data.get("favorites")
        # Удаляем название фильма из списка
        if movie in films:
            films.remove(movie)
        # Сохраняем обновленный список лайкнутых фильмов
        await state.update_data(favorites=films)

        # 2. ищем фильм и удаляем лайк
        for i in self.data["films"]:
            if i["title"] == movie:
                current_likes = i.get("likes", 0)
                i["likes"] = current_likes - 1
            break

        # 3. Сохраняем обновленные данные фильмов
        async with aiofiles.open(self.json_file_path, "w", encoding='utf-8') as fe:
            await fe.write(json.dumps(self.data, ensure_ascii=False, indent=2))

    @staticmethod
    def format_movie(data):
        """Красиво выводим фильм"""
        text = (f"🎬 <b>{data['title']}</b>\n📅 Год: {data['years']}\n⭐ Рейтинг: {data['ratings']}\n"
                f"⏱️ Длительность: {data['duration']}\n🎭 Жанры: {', '.join(data['genres'])}\n────────────")
        if 'trailer_url' in data:
            response_text = f"{text}\n\n📹 <b>Трейлер доступен по ссылке ниже:</b>\n{data['trailer_url']}"
            return response_text
        else:
            response_text = f"{text}\n\n😔 <b>К сожалению, трейлер для этого фильма не найден</b>"
            return response_text
