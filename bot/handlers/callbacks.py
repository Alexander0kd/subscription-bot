from aiogram.fsm.context import FSMContext

from db.crud import get_group_by_join_id
from db.crud.group_crud import mark_payment, leave_group, delete_group, update_group, add_member
from db.models import PaymentStatus
from translation import localize_text
from aiogram import Router, types, F
from bot.keyboards import (
    get_main_keyboard, get_user_group_keyboard, get_admin_settings_keyboard, get_group_members_keyboard,
    get_admin_group_keyboard,
)
from utils import get_localized_group_user, get_localized_joined_groups
from aiogram.fsm.state import StatesGroup, State

router = Router()

@router.callback_query(F.data == "cancel")
async def callback_cancel(callback: types.CallbackQuery, state: FSMContext):
    await state.clear()

    await callback.message.answer(
        localize_text('messages.canceled'),
        reply_markup=get_main_keyboard()
    )

    await callback.answer()


@router.callback_query(F.data.startswith("mark_as_payed:"))
async def handle_mark_as_payed(callback: types.CallbackQuery, pre_user_id: int = None, toggle: bool = False):
    group_id = callback.data.split(":")[1]
    user_id = pre_user_id or callback.from_user.id

    group = await get_group_by_join_id(group_id)

    if not group:
        await callback.message.answer(localize_text('errors.chat_not_found'))
        await callback.answer()
        return

    group.members = sorted(group.members, key=lambda m: 1 if str(m.user_id) == str(user_id) else 0, reverse=True)
    await mark_payment(group, user_id, toggle)

    if not toggle and user_id != group.owner_id:
        await callback.message.bot.send_message(
            chat_id=group.owner_id,
            text=localize_text('messages.admin_payed', user_id=group.owner_tag, name=group.name),
        )

    if toggle:
        await callback.message.edit_text(
            text=get_localized_group_user(group, group.members[0]),
            reply_markup=get_group_members_keyboard(
                payed=group.members[0].status == PaymentStatus.PAID,
                user_id=user_id,
                group_id=group_id,
            )
        )
    else:
        await callback.message.edit_text(
            text=get_localized_joined_groups(group),
            reply_markup=get_user_group_keyboard(
                group.members[0].status,
                group.join_id
            )
        )

    if not toggle and user_id != group.owner_id:
        await callback.message.answer(localize_text('messages.request'))
    await callback.answer()


@router.callback_query(F.data.startswith("leave_group:"))
async def handle_leave_group(callback: types.CallbackQuery, pre_user_id: str = None):
    group_id = callback.data.split(":")[1]
    user_id = pre_user_id or callback.from_user.id

    group = await get_group_by_join_id(group_id)

    if group:
        await leave_group(group, user_id)
        if not pre_user_id:
            await callback.message.edit_text(localize_text('messages.left_group'))
        else:
            await callback.message.answer(localize_text('messages.done'))
    else:
        await callback.message.answer(localize_text('errors.general'))
    await callback.answer()


@router.callback_query(F.data.startswith("settings:"))
async def handle_settings(callback: types.CallbackQuery):
    group_id = callback.data.split(":")[1]

    group = await get_group_by_join_id(group_id)

    if group and callback.from_user.id == group.owner_id:
        await callback.message.edit_reply_markup(
            reply_markup=get_admin_settings_keyboard(group_id)
        )
    else:
        await callback.message.answer(localize_text('errors.general'))
    await callback.answer()


@router.callback_query(F.data.startswith("view_members:"))
async def handle_view_members(callback: types.CallbackQuery):
    group_id = callback.data.split(":")[1]
    group = await get_group_by_join_id(group_id)

    if group and callback.from_user.id == group.owner_id:
        if len(group.members) <= 0:
            await callback.message.answer(text=localize_text('messages.members_not_found'))
            await callback.answer()
            return

        for m in group.members:
            await callback.message.answer(
                text=get_localized_group_user(group, m),
                reply_markup=get_group_members_keyboard(
                    payed=m.status == PaymentStatus.PAID,
                    user_id=m.user_id,
                    group_id=group_id,
                )
            )
    else:
        await callback.message.answer(localize_text('errors.general'))
    await callback.answer()


@router.callback_query(F.data.startswith("delete_group:"))
async def handle_delete_group(callback: types.CallbackQuery):
    group_id = callback.data.split(":")[1]
    group = await get_group_by_join_id(group_id)

    if group and callback.from_user.id == group.owner_id:
        await delete_group(group)

        await callback.message.edit_text(
            localize_text('messages.deleted')
        )
    else:
        await callback.answer(localize_text('errors.general'))
    await callback.answer()


@router.callback_query(F.data.startswith("change_status:"))
async def handle_change_status(callback: types.CallbackQuery):
    user_id = callback.data.split(":")[2]

    await handle_mark_as_payed(callback, user_id, True)


@router.callback_query(F.data.startswith("remove_member:"))
async def handle_remove_member(callback: types.CallbackQuery):
    user_id = callback.data.split(":")[2]

    await handle_leave_group(callback, user_id)


class GroupStates(StatesGroup):
    AWAITING_AMOUNT = State()
    AWAITING_COMMENT = State()

@router.callback_query(F.data.startswith("change_amount:"))
async def handle_change_amount(callback: types.CallbackQuery, state: FSMContext):
    group_id = callback.data.split(":")[1]
    group = await get_group_by_join_id(group_id)

    if group and callback.from_user.id == group.owner_id:
        await state.update_data(group_id=group_id)
        await callback.message.answer(localize_text('messages.enter_new_amount'))
        await state.set_state(GroupStates.AWAITING_AMOUNT)
    else:
        await callback.answer(localize_text('errors.general'))
    await callback.answer()



@router.message(GroupStates.AWAITING_AMOUNT)
async def process_new_amount(message: types.Message, state: FSMContext):
    data = await state.get_data()
    group = await get_group_by_join_id(data['group_id'])

    try:
        amount = float(message.text)
        if amount <= 0:
            await message.answer(localize_text('errors.nan'))
            return

        group.amount = amount
        await update_group(group)
        await message.answer(localize_text('messages.done'))
        await state.clear()
    except ValueError:
        await message.answer(localize_text('errors.nan'))


@router.callback_query(F.data.startswith("change_comment:"))
async def handle_change_comment(callback: types.CallbackQuery, state: FSMContext):
    group_id = callback.data.split(":")[1]
    group = await get_group_by_join_id(group_id)

    if group and callback.from_user.id == group.owner_id:
        await state.update_data(group_id=group_id)
        await callback.message.answer(localize_text('messages.enter_new_comment'))
        await state.set_state(GroupStates.AWAITING_COMMENT)
    else:
        await callback.answer(localize_text('errors.general'))
    await callback.answer()


@router.message(GroupStates.AWAITING_COMMENT)
async def process_new_comment(message: types.Message, state: FSMContext):
    data = await state.get_data()
    group = await get_group_by_join_id(data['group_id'])

    group.description = message.text
    await update_group(group)

    await message.answer(localize_text('messages.done'))
    await state.clear()


@router.callback_query(F.data.startswith("back:"))
async def handle_back(callback: types.CallbackQuery):
    group_id = callback.data.split(":")[1]
    group = await get_group_by_join_id(group_id)

    if group and callback.from_user.id == group.owner_id:
        await callback.message.edit_reply_markup(
            reply_markup=get_admin_group_keyboard(group_id)
        )
    else:
        await callback.message.answer(localize_text('errors.general'))
    await callback.answer()


@router.callback_query(F.data.startswith("reject:"))
async def handle_reject(callback: types.CallbackQuery):
    group_id = callback.data.split(":")[1]
    group = await get_group_by_join_id(group_id)

    if group and callback.from_user.id == group.owner_id:
        await callback.message.edit_reply_markup()
    else:
        await callback.message.answer(localize_text('errors.general'))
    await callback.answer()


@router.callback_query(F.data.startswith("approve:"))
async def handle_approve(callback: types.CallbackQuery):
    group_id = callback.data.split(":")[1]
    user_id = callback.data.split(":")[2]
    user_tag = callback.data.split(":")[3]
    group = await get_group_by_join_id(group_id)

    if group and callback.from_user.id == group.owner_id:
        await add_member(group, user_id, user_tag)

        await callback.message.bot.send_message(
            chat_id=group.owner_id,
            text=localize_text('messages.join_approved', group=group_id),
        )

        await callback.message.edit_reply_markup()
    else:
        await callback.message.answer(localize_text('errors.general'))
    await callback.answer()


@router.callback_query(F.data.startswith("payed:"))
async def handle_payed(callback: types.CallbackQuery):
    await handle_mark_as_payed(callback)
