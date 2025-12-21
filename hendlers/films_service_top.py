import json
import os
import aiofiles

from aiogram.fsm.context import FSMContext

current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
file_path = os.path.join(parent_dir, 'movies.json')

class RatingsFilms:

    def __init__(self, json_file):
        full_path = json_file if os.path.isabs(json_file) else os.path.join(parent_dir, json_file)
        with open(full_path, 'r', encoding='utf-8') as f:
            self.data = json.load(f)
        self.films_rating_list = self.data["films"]
        self.json_file_path = full_path
        self.sorted_films = []
        self.blocks = []
        self.block_size = 10

        # Сортируем и разбиваем на блоки при инициализации
        self._prepare_films()

    def _prepare_films(self):
        """Сортирует фильмы, добавляет нумерацию и разбивает на блоки."""
        # Сортируем
        self.sorted_films = sorted(self.films_rating_list, key=lambda x: x.get('ratings', 0), reverse=True)
        # Добавляем нумерацию
        for i, film in enumerate(self.sorted_films, start=1):
            film["number"] = i
        # Разбиваем на блоки
        self.blocks = []
        for i in range(0, len(self.sorted_films), self.block_size):
            block = self.sorted_films[i:i + self.block_size]
            self.blocks.append(block)

    def get_current_page(self, data: int):
        """Возвращает текущую страницу фильмов"""
        if 0 <= data < len(self.blocks):
            return self.blocks[data]
        else:
            return False

    def number_on_the_list(self, sp):
        """Делаем список с номерами, для проверки правильного номера"""
        final = []
        for i in sp:
            for j, d in i.items():
                if j == 'number':
                    final.append(d)
        return final

    def b(self, sp: list, number):
        """Красивый вывод фильма выбранный пользователем"""
        dano = 0
        for i in sp:
            for j, d in i.items():
                if number == d:
                    dano = i

        text = (f"🎬 <b>{dano['title']}</b>\n📅 Год: {dano['years']}\n⭐ Рейтинг: {dano['ratings']}\n"
                f"⏱️ Длительность: {dano['duration']}\n🎭 Жанры: {', '.join(dano['genres'])}\n────────────")
        if 'trailer_url' in dano:
            response_text = f"{text}\n\n📹 <b>Трейлер доступен по ссылке ниже:</b>\n{dano['trailer_url']}"
            return response_text
        else:
            response_text = f"{text}\n\n😔 <b>К сожалению, трейлер для этого фильма не найден</b>"
            return response_text

    def trailer(self, sp: list, number):
        """Достаем ссылку на трейлер"""
        pr = 0
        for i in sp:
            for j, d in i.items():
                if number == d:
                    pr = i
        if 'trailer_url' in pr:
            return pr['trailer_url']

    async def add_like_to_film(self, sp, number, state: FSMContext):
        """Добавляем лайк фильму"""
        # 1. Находим название фильма
        film = 0
        for i in sp:
            for j, d in i.items():
                if number == d:
                    film = i
                    break
        film_title = film['title']

        # 2. Проверяем, лайкал ли пользователь уже этот фильм
        data = await state.get_data()
        list_favorites = data.get("favorites")
        if list_favorites is None:
            list_favorites = []

        film_title_lower = film_title.lower()

        for i in list_favorites:
            if i.lower() == film_title_lower:
                return None

        # 3. Если пользователь не лайкал этот фильм, обновляем список в состоянии
        list_favorites.append(film_title)
        await state.update_data(favorites=list_favorites)

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

    def format_page(self, films):
        """Делаем красивый вывод для пользователя"""
        text = ""
        for film in films:
            text += f"{film['number']}. 🎬<b>{film['title']}</b>\n"
            text += f"📅Год: {film['years']}\n⭐️Рейтинг: {film['ratings']}/10\n⏱️Длительность: {film['duration']}\n"
            text += f"🎭Жанры: {', '.join(film['genres'])}\n\n"
        return text
