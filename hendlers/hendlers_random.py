from aiogram import Router
from aiogram.filters import StateFilter
from aiogram.types import Message, CallbackQuery

from .states import GeneralConditions
from keyboards.keyboards import *
from .film_random import *



router = Router()
user = RandomFilm("movies.json")

# Обрабатываем хэндлер рандомного фильма
@router.callback_query(GeneralConditions.random_film)
async def pick_random_movie(callback: CallbackQuery, state: FSMContext):
    pass