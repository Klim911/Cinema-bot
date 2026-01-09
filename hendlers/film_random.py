import json
import os
import random
import aiofiles


class RandomFilm:

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

    async def add_like_random_film(self, state):
        """Добавляем лайк фильму"""

        # 1. Достаем из состояния фильм
        data = await state.get_data()
        film = data.get("random_film")
        film_title = film['title']          # название фильма

        # 2. Проверяем, лайкал ли пользователь уже этот фильм
        list_favorites = data.get("favorites")
        if list_favorites is None:
            list_favorites = []

        film_title_lower = film_title.lower()

        for i in list_favorites:
            if i.lower() == film_title_lower:
                return None

        # 3. Если пользователь не лайкал этот фильм, обновляем список в состоянии
        list_favorites.append(film_title)
        print(list_favorites)
        await state.update_data(favorites=list_favorites)
        list_favorites1 = data.get("favorites")
        print(list_favorites1)

        # 4. Ищем фильм и добавляем лайк
        film_found = False
        new_likes = 0

        for i in self.data["films"]:
            if i["title"].lower() == film_title_lower:
                i["likes"] = i.get("likes", 0) + 1
                new_likes = i["likes"]
                film_found = True
                break

        if not film_found:
            return None

        # 5. Сохраняем обновленные данные фильмов
        async with aiofiles.open(self.json_file_path, "w", encoding='utf-8') as fe:
            await fe.write(json.dumps(self.data, ensure_ascii=False, indent=2))

        return new_likes
