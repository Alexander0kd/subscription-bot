from translation import localize_text
from aiogram import Router, types, F
from bot.keyboards import *

router = Router()

@router.message(F.text == localize_text('menu.joined'))
async def handle_btn_joined(message: types.Message):
    """Обробник текстових повідомлень"""
    await message.answer(
        localize_text('1'),
        reply_markup=get_back_button()
    )

@router.message(F.text == localize_text('menu.groups'))
async def handle_btn_groups(message: types.Message):
    """Обробник текстових повідомлень"""
    await message.answer(
        localize_text('2'),
        reply_markup=get_main_keyboard()
    )

@router.message(F.text == localize_text('menu.create'))
async def handle_btn_create(message: types.Message):
    """Обробник текстових повідомлень"""
    await message.answer(
        localize_text('3'),
        reply_markup=get_main_keyboard()
    )

@router.message(F.text)
async def handle_default(message: types.Message):
    """Обробник текстових повідомлень"""
    await message.answer(
        localize_text('errors.unknown_command'),
        reply_markup=get_main_keyboard()
    )
