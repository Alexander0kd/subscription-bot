from aiogram import types

from bot.keyboards import get_user_group_keyboard
from db.crud import get_by_member
from db.utils import get_displayed_date
from translation import localize_text


async def get_my_joined_groups(message: types.Message):
    """Початок створення групи"""
    groups = await get_by_member(message.from_user.id)

    if len(groups) <= 0:
        await message.answer(text=localize_text('messages.group_not_found'))
        return

    await message.answer(text=localize_text('messages.group_list'))
    for group_data in groups:
        await message.answer(
            text=get_localized_group_user(group_data),
            reply_markup=get_user_group_keyboard(
                group_data.members[0].status,
                group_data.join_id
            )
        )


def get_localized_group_user(group) -> str:
    user = group.members[0]
    next_payment_date = group.get_next_payment_date(user)

    localized_period = localize_text(f"buttons.{group.payment_period.replace('.PaymentPeriod.', '.')}")
    localized_period_order = localize_text(f"buttons.{group.payment_method.replace('.PaymentMethod.', '.')}")

    return localize_text(
        'messages.group_user',
        name=group.name,
        owner=group.owner_tag,
        status=localize_text(f"buttons.{user.status.replace('.PaymentStatus.', '.')}"),
        date=get_displayed_date(next_payment_date),
        period=localized_period,
        period_order=localized_period_order,
        sum=group.amount,
        comment=group.description
    )