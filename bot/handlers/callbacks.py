from translation import localize_text
from aiogram import Router, types, F
from bot.keyboards import (
    get_main_keyboard,
)

router = Router()

@router.callback_query(F.data == "back")
async def callback_joined_menu(callback: types.CallbackQuery):
    """Кнопка joined"""
    await callback.message.answer(
        localize_text('Мої підписки'),
        reply_markup=get_main_keyboard()
    )
    await callback.answer()
