from datetime import datetime

from bot.chrono.chrono_module import daily_payment_check
from config import DEV_USER_ID
from translation import localize_text
from bot.keyboards import get_main_keyboard
from aiogram import types


async def handle_chrono(message: types.Message):
    user_id = message.from_user.id

    if user_id != DEV_USER_ID:
        await message.answer(
            localize_text('commands.chrono.no_access'),
            reply_markup=get_main_keyboard()
        )
        return
    else:
        await message.answer(
            localize_text('commands.chrono.proceed', date=datetime.now().isoformat()),
            reply_markup=get_main_keyboard()
        )

        from bot.bot import bot
        await daily_payment_check(bot)
