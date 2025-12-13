import json
import os


current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
file_path = os.path.join(parent_dir, 'movies.json')

class RatingsFilms:

    def __init__(self, json_file):
        full_path = json_file if os.path.isabs(json_file) else os.path.join(parent_dir, json_file)
        with open(full_path, 'r', encoding='utf-8') as f:
            self.data = json.load(f)
        self.films_rating_list = self.data["films"]
        self.sorted_films = []
        self.blocks = []
        self.current_page = 0
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

    def get_current_page(self):
        """Возвращает текущую страницу фильмов"""
        if 0 <= self.current_page < len(self.blocks):
            return self.blocks[self.current_page]

    def next_page(self):
        """Переходит на следующую страницу"""
        if self.current_page < len(self.blocks) - 1:
            self.current_page += 1
            return self.get_current_page()

    def prev_page(self):
        """Переходит на предыдущую страницу"""
        if self.current_page > 0:
            self.current_page -= 1
            return self.get_current_page()

    def format_page(self, films):
        pass


dt = RatingsFilms("movies.json")
print(dt.blocks)