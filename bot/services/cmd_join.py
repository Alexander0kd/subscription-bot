from db.crud import get_group_by_join_id
from translation import localize_text
from bot.keyboards import get_main_keyboard, get_admin_join_keyboard
from aiogram import types


async def handle_join(message: types.Message):
    join_id = message.text.split()[1] if len(message.text.split()) > 1 else None
    if not join_id:
        await message.answer(
            localize_text('commands.join.error_id'),
            reply_markup=get_main_keyboard()
        )
        return

    group = await get_group_by_join_id(join_id)
    if not group:
        await message.answer(
            text=localize_text('commands.join.error_group'),
            reply_markup=get_main_keyboard()
        )
        return


    if group.owner_id:
        can_join = not(any(member.user_id == message.from_user.id for member in group.members) or
                     group.owner_id == message.from_user.id)

        if not can_join:
            await message.answer(
                localize_text('commands.join.restrict'),
                reply_markup=get_main_keyboard()
            )
            return

        username = message.from_user.username
        full_name = message.from_user.full_name
        user_id = message.from_user.id
        owner_tag = f"@{username}" if username else full_name or str(user_id)

        await message.bot.send_message(
            chat_id=group.owner_id,
            text=localize_text('commands.join.request', name=group.name, user=owner_tag),
            reply_markup=get_admin_join_keyboard(user_id, join_id, owner_tag)
        )

        await message.answer(
            localize_text('commands.join.wait', name=group.name),
            reply_markup=get_main_keyboard()
        )
    else:
        await message.answer(
            localize_text('errors.general'),
            reply_markup=get_main_keyboard()
        )