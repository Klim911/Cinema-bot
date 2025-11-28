from aiogram import F, Router, types
from aiogram.filters import Command, CommandStart, StateFilter
from aiogram import Router
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup, default_state
from aiogram.types import Message, ContentType

from lexicon.lexicon import LEXICON
from states import GeneralConditions


router = Router()
"""Обрабатываем команду start"""
# Этот хэндлер будет срабатывать на команду /start вне состояний и предлагать сделать выбор нажатия одной из кнопок
# главного меню
@router.message(CommandStart(), StateFilter(default_state))
async def process_start_command(message: Message):
    await message.answer(text=LEXICON["/start"])

"""Обрабатываем команду help"""
# Этот хэндлер будет срабатывать на команду /help в состоянии по умолчанию и сообщать
# что вы можете сейчас сделать
@router.message(Command(commands="/help"), StateFilter(default_state))
async def process_help_command(message: Message):
    await message.answer(text=LEXICON["help"])

# # Этот хэндлер будет срабатывать на команду "cancel" в любых состояниях, кроме состояния по умолчанию и выполнять
# # действие назад.
# @router.message(Command(commands="cancel"), ~StateFilter(default_state))
# async def process_cancel_command(massage: Message, state: FSMContext):
#     pass

# Этот хэндлер будет срабатывать на команду "go" и переводить бота в состояние первого выбора в главном меню,
# после отправки этой команды, для пользователя откроются кнопки
@router.message((F.text == LEXICON["go"]), StateFilter(default_state))
async def process_go_command(message: Message, state: FSMContext):
    await message.answer(text=LEXICON["go"])
    # Устанавливаем состояние первого выбора в главном меню
    await state.set_state(GeneralConditions.first_choice)

# Этот хэндлер будет срабатывать на любые сообщения, кроме тех
# для которых есть отдельные хэндлеры, вне состояний
@router.message(StateFilter(default_state))
async def send_echo(message: Message):
    await message.answer(text=LEXICON["no"])