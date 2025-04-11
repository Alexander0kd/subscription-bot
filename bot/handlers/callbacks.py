from aiogram.fsm.context import FSMContext

from db.crud import get_group_by_join_id
from db.crud.group_crud import mark_payment, leave_group, delete_group
from db.models import PaymentStatus
from translation import localize_text
from aiogram import Router, types, F
from bot.keyboards import (
    get_main_keyboard, get_user_group_keyboard, get_admin_settings_keyboard, get_group_members_keyboard,
)
from utils import get_displayed_date, get_localized_group_user

router = Router()

@router.callback_query(F.data == "cancel")
async def callback_cancel(callback: types.CallbackQuery, state: FSMContext):
    """Кнопка Cancel"""
    await state.clear()

    await callback.message.answer(
        localize_text('messages.canceled'),
        reply_markup=get_main_keyboard()
    )

    await callback.answer()


@router.callback_query(F.data.startswith("mark_as_payed:"))
async def handle_mark_as_payed(callback: types.CallbackQuery):
    group_id = callback.data.split(":")[1]
    user_id = callback.from_user.id

    group = await get_group_by_join_id(group_id)

    if not group:
        await callback.message.answer(localize_text('errors.chat_not_found'))
        await callback.answer()
        return

    await mark_payment(group, user_id)

    await callback.message.bot.send_message(
        chat_id=group.owner_id,
        text=localize_text('messages.admin_payed', user_id=group.owner_tag),
    )

    await callback.message.edit_reply_markup(
        reply_markup=get_user_group_keyboard(PaymentStatus.PAID, group_id)
    )

    await callback.message.answer(localize_text('messages.request'))
    await callback.answer()


@router.callback_query(F.data.startswith("leave_group:"))
async def handle_leave_group(callback: types.CallbackQuery):
    group_id = callback.data.split(":")[1]
    user_id = callback.from_user.id

    group = await get_group_by_join_id(group_id)

    if group:
        await leave_group(group, user_id)
        await callback.message.edit_text(localize_text('messages.left_group'))
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
    group_id = callback.data.split(":")[1]
    user_id = callback.data.split(":")[2]
    await callback.answer(localize_text('errors.general'))


@router.callback_query(F.data.startswith("remove_member:"))
async def handle_remove_member(callback: types.CallbackQuery):
    group_id = callback.data.split(":")[1]
    user_id = callback.data.split(":")[2]
    await callback.answer(localize_text('errors.general'))


@router.callback_query(F.data.startswith("change_amount:"))
async def handle_change_amount(callback: types.CallbackQuery):
    group_id = callback.data.split(":")[1]
    await callback.answer(localize_text('errors.general'))


@router.callback_query(F.data.startswith("change_comment:"))
async def handle_change_comment(callback: types.CallbackQuery):
    group_id = callback.data.split(":")[1]
    await callback.answer(localize_text('errors.general'))


@router.callback_query(F.data.startswith("back:"))
async def handle_back(callback: types.CallbackQuery):
    group_id = callback.data.split(":")[1]
    await callback.answer(localize_text('errors.general'))


@router.callback_query(F.data.startswith("reject:"))
async def handle_reject(callback: types.CallbackQuery):
    group_id = callback.data.split(":")[1]
    user_id = callback.data.split(":")[2]
    await callback.answer(localize_text('errors.general'))


@router.callback_query(F.data.startswith("approve:"))
async def handle_approve(callback: types.CallbackQuery):
    group_id = callback.data.split(":")[1]
    user_id = callback.data.split(":")[2]
    await callback.answer(localize_text('errors.general'))


@router.callback_query(F.data.startswith("payed:"))
async def handle_payed(callback: types.CallbackQuery):
    group_id = callback.data.split(":")[1]
    await callback.answer(localize_text('errors.general'))
