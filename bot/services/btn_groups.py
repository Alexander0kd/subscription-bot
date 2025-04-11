from aiogram import types

from bot.keyboards import get_admin_group_keyboard
from db.crud import get_by_owner
from db.models import PaymentStatus
from utils import get_displayed_date
from translation import localize_text


async def get_my_groups(message: types.Message):
    """Початок створення групи"""
    groups = await get_by_owner(message.from_user.id)

    if len(groups) <= 0:
        await message.answer(text=localize_text('messages.group_not_found'))
        return

    await message.answer(text=localize_text('messages.group_list'))
    for group_data in groups:
        await message.answer(
            text=get_localized_group_admin(group_data),
            reply_markup=get_admin_group_keyboard(group_data.join_id)
        )


def get_localized_group_admin(group) -> str:
    user_count = len(group.members)
    paid_count = len([member for member in group.members if dict(member.to_dict()).get('status') == PaymentStatus.PAID])

    localized_period = localize_text(f"buttons.{group.payment_period.replace('.PaymentPeriod.', '.')}")
    localized_period_order = localize_text(f"buttons.{group.payment_method.replace('.PaymentMethod.', '.')}")
    status = f"{paid_count}/{user_count}"

    return localize_text(
        'messages.group_admin',
        name=group.name,
        date=get_displayed_date(group.current_payment_date),
        user_count=user_count,
        sum=group.amount,
        status=status,
        period=localized_period,
        period_order=localized_period_order,
        comment=group.description,
        id=group.join_id
    )