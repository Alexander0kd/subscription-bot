from bot.keyboards.builder import *

def get_main_keyboard() -> ReplyKeyboardMarkup:
    """Повертає основну клавіатуру меню"""
    return build_reply_keyboard(
        buttons=[
            {"text": "menu.joined"},
            {"text": "menu.groups"},
            {"text": "menu.create"}
        ],
        row_width=2
    )

def get_back_button() -> InlineKeyboardMarkup:
    """Повертає кнопку 'Назад'"""
    return build_inline_keyboard(
        buttons=[
            {
                "text": "main.menu.back",
                "callback_data": "back"
            }
        ],
        row_width=1
    )
