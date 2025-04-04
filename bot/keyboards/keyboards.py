from db.models import PaymentPeriod
from translation import localize_text

from aiogram.types import ReplyKeyboardMarkup, InlineKeyboardMarkup
from bot.keyboards.builder import build_inline_keyboard, build_reply_keyboard

__all__ = [
    'get_main_keyboard',
    'get_user_group_keyboard',
    'get_admin_group_keyboard',
    'get_admin_settings_keyboard',
    'get_period_create_keyboard',
    'get_period_settings_keyboard',
    'get_order_create_keyboard',
    'get_order_settings_keyboard',
    'get_group_members_keyboard',
    'get_admin_join_keyboard',
    'get_confirm_keyboard',
    'get_cancel_keyboard',
    'get_mark_as_paid_keyboard',
    'get_confirm_payed_keyboard',
    'get_remove_member_keyboard'
]

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

def get_user_group_keyboard(payed: bool, group_id: str) -> InlineKeyboardMarkup:
    """Повертає клавіатуру з кнопками 'Відмитити як оплачену' та 'Покинути групу'"""
    buttons = []
    if payed:
        buttons.append({
            "text": "buttons.mark_as_payed",
            "callback_data": f"mark_as_payed:{group_id}"
        })

    buttons.append({
        "text": "buttons.leave_group",
        "callback_data": f"leave_group:{group_id}"
    })

    return build_inline_keyboard(
        buttons=buttons,
        row_width=1
    )


def get_admin_group_keyboard(group_id: str) -> InlineKeyboardMarkup:
    """Повертає клавіатуру з кнопками 'Налаштування', 'Переглянути учасників' та 'Видалити групу'"""
    return build_inline_keyboard(
        buttons=[
            {
                "text": "buttons.settings",
                "callback_data": f"settings:{group_id}"
            },
            {
                "text": "buttons.view_members",
                "callback_data": f"view_members:{group_id}"
            },
            {
                "text": "buttons.delete_group",
                "callback_data": f"delete_group:{group_id}"
            }
        ],
        row_width=1
    )


def get_admin_settings_keyboard(group_id: str) -> InlineKeyboardMarkup:
    """Повертає клавіатуру з кнопками 'change_date', 'change_amount', 'change_payment_period' та 'change_comment'"""
    return build_inline_keyboard(
        buttons=[
            {
                "text": "buttons.change_date",
                "callback_data": f"change_date:{group_id}"
            },
            {
                "text": "buttons.change_amount",
                "callback_data": f"change_amount:{group_id}"
            },
            {
                "text": "buttons.change_payment_period",
                "callback_data": f"change_payment_period:{group_id}"
            },
            {
                "text": "buttons.change_comment",
                "callback_data": f"change_comment:{group_id}"
            }
        ],
        row_width=1
    )


def get_period_create_keyboard() -> InlineKeyboardMarkup:
    """Повертає клавіатуру з кнопками 'daily', 'weekly' та 'monthly'"""
    return build_inline_keyboard(
        buttons=[
            {
                "text": "buttons.daily",
                "callback_data": PaymentPeriod.DAILY
            },
            {
                "text": "buttons.weekly",
                "callback_data": PaymentPeriod.WEEKLY
            },
            {
                "text": "buttons.monthly",
                "callback_data": PaymentPeriod.MONTHLY
            },
            {
                "text": "buttons.cancel",
                "callback_data": "cancel"
            }
        ],
        row_width=1
    )


def get_period_settings_keyboard(group_id: str) -> InlineKeyboardMarkup:
    """Повертає клавіатуру з кнопками 'daily', 'weekly' та 'monthly'"""
    return build_inline_keyboard(
        buttons=[
            {
                "text": "buttons.daily",
                "callback_data": f"{PaymentPeriod.DAILY}:{group_id}"
            },
            {
                "text": "buttons.weekly",
                "callback_data": f"{PaymentPeriod.WEEKLY}:{group_id}"
            },
            {
                "text": "buttons.monthly",
                "callback_data": f"{PaymentPeriod.MONTHLY}:{group_id}"
            }
        ],
        row_width=1
    )


def get_order_create_keyboard() -> InlineKeyboardMarkup:
    """Повертає клавіатуру з кнопками 'from_each_user', 'in_turn_randomly' та 'in_turn_by_join_date'"""
    return build_inline_keyboard(
        buttons=[
            {
                "text": "buttons.from_each_user",
                "callback_data": "from_each_user"
            },
            {
                "text": "buttons.in_turn_randomly",
                "callback_data": "in_turn_randomly"
            },
            {
                "text": "buttons.in_turn_by_join_date",
                "callback_data": "in_turn_by_join_date"
            },
            {
                "text": "buttons.cancel",
                "callback_data": "cancel"
            }
        ],
        row_width=1
    )


def get_order_settings_keyboard(group_id: str) -> InlineKeyboardMarkup:
    """Повертає клавіатуру з кнопками 'from_each_user', 'in_turn_randomly' та 'in_turn_by_join_date'"""
    return build_inline_keyboard(
        buttons=[
            {
                "text": "buttons.from_each_user",
                "callback_data": f"from_each_user:{group_id}"
            },
            {
                "text": "buttons.in_turn_randomly",
                "callback_data": f"in_turn_randomly:{group_id}"
            },
            {
                "text": "buttons.in_turn_by_join_date",
                "callback_data": f"in_turn_by_join_date:{group_id}"
            }
        ],
        row_width=1
    )


def get_group_members_keyboard(payed: bool, user_id: str, group_id: str) -> InlineKeyboardMarkup:
    """Повертає клавіатуру з кнопками 'change_status', 'change_payment_date' та 'remove_member'"""
    status_text = localize_text('buttons.change_status', status="payed" if payed else "unpaid")
    return build_inline_keyboard(
        buttons=[
            {
                "text": status_text,
                "callback_data": f"change_status:{group_id}:{user_id}"
            },
            {
                "text": "buttons.change_payment_date",
                "callback_data": f"change_payment_date:{group_id}:{user_id}"
            },
            {
                "text": "buttons.remove_member",
                "callback_data": f"remove_member:{group_id}:{user_id}"
            }
        ],
        row_width=1
    )


def get_admin_join_keyboard() -> InlineKeyboardMarkup:
    """Повертає клавіатуру з кнопками 'Відхилити' та 'Додати'"""
    return build_inline_keyboard(
        buttons=[
            {
                "text": "buttons.reject",
                "callback_data": "reject"
            },
            {
                "text": "buttons.approve",
                "callback_data": "approve"
            }
        ],
        row_width=2
    )


def get_confirm_keyboard() -> InlineKeyboardMarkup:
    """Повертає клавіатуру з кнопками 'Ні' та 'Так'"""
    return build_inline_keyboard(
        buttons=[
            {
                "text": "buttons.no",
                "callback_data": "no"
            },
            {
                "text": "buttons.yes",
                "callback_data": "yes"
            }
        ],
        row_width=2
    )


def get_cancel_keyboard() -> InlineKeyboardMarkup:
    """Повертає клавіатуру з кнопками 'Скасувати'"""
    return build_inline_keyboard(
        buttons=[
            {
                "text": "buttons.cancel",
                "callback_data": "cancel"
            }
        ],
        row_width=1
    )


def get_mark_as_paid_keyboard(group_id: str) -> InlineKeyboardMarkup:
    """Повертає клавіатуру з кнопками 'Оплачено'"""
    return build_inline_keyboard(
        buttons=[
            {
                "text": "buttons.payed",
                "callback_data": f"payed:{group_id}"
            }
        ],
        row_width=1
    )


def get_confirm_payed_keyboard(user_id: str, group_id: str) -> InlineKeyboardMarkup:
    """Повертає клавіатуру з кнопками 'Підтвердити'"""
    return build_inline_keyboard(
        buttons=[
            {
                "text": "buttons.confirm",
                "callback_data": f"confirm:{group_id}:{user_id}"
            }
        ],
        row_width=1
    )


def get_remove_member_keyboard(user_id: str, group_id: str) -> InlineKeyboardMarkup:
    """Повертає клавіатуру з кнопками 'Видалити учасника'"""
    return build_inline_keyboard(
        buttons=[
            {
                "text": "buttons.remove_member",
                "callback_data": f"remove_member:{group_id}:{user_id}"
            }
        ],
        row_width=1
    )