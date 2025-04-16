from aiogram.utils.keyboard import InlineKeyboardBuilder, ReplyKeyboardBuilder

from translation import localize_text
from typing import List, Dict, Union, Optional
from aiogram.types import (
    InlineKeyboardMarkup,
    InlineKeyboardButton,
    ReplyKeyboardMarkup,
    KeyboardButton, ReplyKeyboardRemove
)

__all__ = ['build_inline_keyboard', 'build_reply_keyboard']

def build_inline_keyboard(
        buttons: List[Dict[str, Union[str, Dict]]],
        row_width: int = 2,
        adjust: Optional[List[int]] = None
) -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()

    for button in buttons:
        text = localize_text(button['text'])

        if 'url' in button:
            kb_button = InlineKeyboardButton(text=text, url=button['url'])
        else:
            kb_button = InlineKeyboardButton(
                text=text,
                callback_data=button['callback_data']
            )

        builder.add(kb_button)

        if adjust:
            builder.adjust(*adjust)
        else:
            builder.adjust(row_width)

    return builder.as_markup()


def build_reply_keyboard(
        buttons: List[Union[str, Dict[str, str]]],
        row_width: int = 2,
        resize_keyboard: bool = True,
        one_time_keyboard: bool = False,
        adjust: Optional[List[int]] = None
) -> ReplyKeyboardRemove | ReplyKeyboardMarkup:
    if not buttons:
        return ReplyKeyboardRemove()

    builder = ReplyKeyboardBuilder()

    for button in buttons:
        if isinstance(button, dict):
            rp_button = KeyboardButton(text=localize_text(button['text']))
        else:
            rp_button = KeyboardButton(text=localize_text(button))

        builder.add(rp_button)

        if adjust:
            builder.adjust(*adjust)
        else:
            builder.adjust(row_width)

    return builder.as_markup(
        resize_keyboard=resize_keyboard,
        one_time_keyboard=one_time_keyboard,
    )
