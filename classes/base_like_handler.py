import json
import aiofiles
from pathlib import Path
from config.config import MOVIES_JSON


class BaseFilmLike:

    def __init__(self, json_file=None):
        if json_file is None:
            self.json_file_path = MOVIES_JSON
        else:
            self.json_file_path = Path(json_file) if isinstance(json_file, str) else json_file
        self.films_list = None

    async def load_films(self):
        # Загружаем базу фильмов из JSON файла
        async with aiofiles.open(self.json_file_path, "r", encoding="utf-8") as f:
            data = json.loads(await f.read())
            self.films_list = data["films"]
            return self.films_list

    async def add_like_to_film(self, title, state):
        # 1. Определяем состояние
        user_choice = await state.get_data()

        # 2. Проверяем, лайкал ли пользователь уже этот фильм
        list_favorites = user_choice.get("favorites")
        print(list_favorites)
        if list_favorites is None:
            list_favorites = []

        film_title_lower = title.lower()
        print(film_title_lower)
        for i in list_favorites:
            if i.lower() == film_title_lower:
                return None

        # 3. Если пользователь не лайкал этот фильм, обновляем список в состоянии
        list_favorites.append(title)
        await state.update_data(favorites=list_favorites)

        # 4. Ищем фильм и добавляем лайк
        film_found = False
        new_likes = 0
        self.films_list = await self.load_films()

        for i in self.films_list:
            if i["title"].lower() == film_title_lower:
                i["likes"] = i.get("likes", 0) + 1
                new_likes = i["likes"]
                film_found = True
                break

        if not film_found:
            return None

        # 5. Сохраняем обновленные данные фильмов
        data_to_save = {"films": self.films_list}
        async with aiofiles.open(self.json_file_path, "w", encoding='utf-8') as fe:
            await fe.write(json.dumps(data_to_save, ensure_ascii=False, indent=2))

        return new_likes
