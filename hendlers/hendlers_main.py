from aiogram.filters import Command, CommandStart, StateFilter
from aiogram import Router
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import default_state
from aiogram.types import Message, ReplyKeyboardRemove

from lexicon.lexicon import LEXICON
from .states import GeneralConditions
from keyboards.keyboards import *


router = Router()


# Этот хэндлер будет срабатывать на команду /start вне состояний и предлагать сделать выбор нажатия одной из кнопок
# главного меню
@router.message(CommandStart())
async def process_start_command(message: Message, state: FSMContext):
    # Получаем ID пользователя
    user_id = message.from_user.id
    # Сохраняем ID пользователя в состояние
    await state.update_data(user_id=user_id)
    # Выводим сообщение
    await message.answer(text=LEXICON["/start"], reply_markup=main_builder)
    # Устанавливаем состояние первого выбора в главном меню
    await state.set_state(GeneralConditions.first_choice)


"""Обрабатываем команду help"""
# Этот хэндлер будет срабатывать на команду /help в состоянии по умолчанию и сообщать
# что вы можете сейчас сделать
@router.message(Command(commands="/help"), StateFilter(default_state))
async def process_help_command(message: Message):
    await message.answer(text=LEXICON["help"],  reply_markup=ReplyKeyboardRemove())


@router.message(StateFilter(default_state))
async def process_unknown_message(message: Message, state: FSMContext):
    await message.answer(text=LEXICON["please"], reply_markup=main_builder)
