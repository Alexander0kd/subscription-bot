from translation import localize_text
from bot.keyboards import get_main_keyboard
from aiogram import types, Router
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext

router = Router()

@router.message(Command("start"))
async def cmd_start(message: types.Message, state: FSMContext):
    """Обробник команди /start"""
    await state.clear()

    # user = await user_db.get_or_create(telegram_id=message.from_user.id)

    await message.answer(
        localize_text('start.welcome', name=message.from_user.full_name or message.from_user.username or message.from_user.id),
        reply_markup=get_main_keyboard()
    )


@router.message(Command("join"))
async def cmd_join(message: types.Message, state: FSMContext):
    """Обробник команди /join"""
    await message.answer(
        localize_text('join.wait', name='Замінити це'),
        reply_markup=get_main_keyboard()
    )
