from aiogram.fsm.context import FSMContext

from translation import localize_text
from aiogram import Router, types, F
from bot.keyboards import (
    get_main_keyboard,
)

router = Router()

@router.callback_query(F.data == "cancel")
async def callback_cancel(callback: types.CallbackQuery, state: FSMContext):
    """Кнопка Cancel"""
    await state.clear()

    await callback.message.answer(
        localize_text('messages.canceled'),
        reply_markup=get_main_keyboard()
    )

    await callback.answer()
