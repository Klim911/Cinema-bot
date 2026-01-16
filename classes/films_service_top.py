import json
from pathlib import Path

from config.config import MOVIES_JSON
from classes.base_like_handler import BaseFilmLike


class RatingsFilms(BaseFilmLike):

    def __init__(self, json_file):
        # pylint: disable=super-init-not-called
        # flake8: noqa
        if json_file is None:
            self.json_file_path = MOVIES_JSON
        else:
            self.json_file_path = Path(json_file) if isinstance(json_file, str) else json_file
        # Загружаем базу фильмов из JSON файла
        with open(self.json_file_path, 'r', encoding='utf-8') as f:
            self.data = json.load(f)
        self.films_rating_list = self.data["films"]
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

    @staticmethod
    def number_on_the_list(sp):
        """Делаем список с номерами, для проверки правильного номера"""
        final = []
        for i in sp:
            for j, d in i.items():
                if j == 'number':
                    final.append(d)
        return final

    @staticmethod
    async def beautiful_format_movie(sp: list, number, state):
        """Красивый вывод фильма выбранный пользователем"""
        dano = 0
        for i in sp:
            for j, d in i.items():
                if number == d:
                    dano = i
        title_film = dano['title']
        await state.update_data(title_film=title_film)
        text = (f"🎬 <b>{dano['title']}</b>\n📅 Год: {dano['years']}\n⭐ Рейтинг: {dano['ratings']}\n"
                f"⏱️ Длительность: {dano['duration']}\n🎭 Жанры: {', '.join(dano['genres'])}\n────────────")
        if 'trailer_url' in dano:
            response_text = f"{text}\n\n📹 <b>Трейлер доступен по ссылке ниже:</b>\n{dano['trailer_url']}"
            return response_text
        else:
            response_text = f"{text}\n\n😔 <b>К сожалению, трейлер для этого фильма не найден</b>"
            return response_text

    @staticmethod
    def trailer(sp: list, number):
        """Достаем ссылку на трейлер"""
        pr = 0
        for i in sp:
            for j, d in i.items():
                if number == d:
                    pr = i
        if 'trailer_url' in pr:
            return pr['trailer_url']

    @staticmethod
    def format_page(films):
        """Делаем красивый вывод для пользователя"""
        text = ""
        for film in films:
            text += f"{film['number']}. 🎬<b>{film['title']}</b>\n"
            text += f"📅Год: {film['years']}\n⭐️Рейтинг: {film['ratings']}/10\n⏱️Длительность: {film['duration']}\n"
            text += f"🎭Жанры: {', '.join(film['genres'])}\n\n"
        return text
