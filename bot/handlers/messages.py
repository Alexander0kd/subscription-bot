from aiogram.filters import StateFilter
from aiogram.fsm.context import FSMContext

from bot.services import create_group, get_my_groups, get_my_joined_groups
from translation import localize_text
from aiogram import Router, types, F
from bot.keyboards import *


router = Router()


@router.message(F.text == localize_text('menu.joined'))
async def handle_btn_joined(message: types.Message, state: FSMContext):
    """Обробник текстових повідомлень"""
    await state.clear()
    await get_my_joined_groups(message)


@router.message(F.text == localize_text('menu.groups'))
async def handle_btn_groups(message: types.Message, state: FSMContext):
    """Обробник текстових повідомлень"""
    await state.clear()
    await get_my_groups(message)


@router.message(F.text == localize_text('menu.create'))
async def handle_btn_create(message: types.Message, state: FSMContext):
    """Обробник текстових повідомлень"""
    await state.clear()
    await create_group(message, state)


@router.message(StateFilter(None), F.text)
async def handle_default(message: types.Message):
    """Обробник текстових повідомлень"""
    await message.answer(
        localize_text('errors.unknown_command'),
        reply_markup=get_main_keyboard()
    )
