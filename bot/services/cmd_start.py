from translation import localize_text
from bot.keyboards import get_main_keyboard
from aiogram import types


async def handle_start(message: types.Message):
    # user = await user_db.get_or_create(telegram_id=message.from_user.id)
    print('test')

    await message.answer(
        localize_text('commands.start.welcome', name=message.from_user.full_name or message.from_user.username or message.from_user.id),
        reply_markup=get_main_keyboard()
    )
