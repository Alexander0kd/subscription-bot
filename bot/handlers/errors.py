from translation import localize_text
from bot.keyboards import get_main_keyboard
from typing import Optional
from aiogram.exceptions import TelegramBadRequest
from aiogram import Router
from aiogram.types import ErrorEvent, Message

router = Router()

async def get_error_message(event: ErrorEvent) -> Optional[Message]:
    """Отримуємо об'єкт повідомлення для відповіді на помилку"""
    if event.update.message:
        return event.update.message
    elif event.update.callback_query and event.update.callback_query.message:
        return event.update.callback_query.message
    return None

@router.error()
async def error_handler(event: ErrorEvent):
    """Глобальний обробник помилок"""
    error = event.exception
    print(error)

    message = await get_error_message(event)
    if not message:
        return

    # Обробка специфічних помилок
    if isinstance(error, TelegramBadRequest):
        return await handle_general_error(message)

    # Загальна помилка
    return await handle_general_error(message)


async def handle_general_error(message: Message):
    """Обробка помилок запиту"""
    await message.answer(
        localize_text('errors.general'),
        reply_markup=get_main_keyboard()
    )
