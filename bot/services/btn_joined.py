from aiogram import types

from bot.keyboards import get_user_group_keyboard
from db.crud import get_by_member
from utils import get_displayed_date, get_localized_joined_groups
from translation import localize_text


async def get_my_joined_groups(message: types.Message):
    groups = await get_by_member(message.from_user.id)

    if len(groups) <= 0:
        await message.answer(text=localize_text('messages.group_not_found'))
        return

    await message.answer(text=localize_text('messages.group_list'))
    for group_data in groups:
        await message.answer(
            text=get_localized_joined_groups(group_data),
            reply_markup=get_user_group_keyboard(
                group_data.members[0].status,
                group_data.join_id
            )
        )

