from aiogram import Bot

from bot.keyboards import get_mark_as_paid_keyboard, get_remove_member_keyboard
from db.models import GroupModel
from translation import localize_text
from utils import get_displayed_date


async def send_reminders(bot: Bot, group: GroupModel):
    for member in group.members:
        if group.should_user_pay(member):
            try:
                await bot.send_message(
                    chat_id=member.user_id,
                    text=localize_text('messages.pay_notification', name=group.name),
                    reply_markup = get_mark_as_paid_keyboard(group.join_id)
                )

                await bot.send_message(
                    chat_id=group.owner_id,
                    text=localize_text('messages.pay_delay', user_tag=member.user_tag, name=group.name),
                    reply_markup=get_remove_member_keyboard(member.user_id, group.join_id)
                )
            except Exception as e:
                print(f"Error: {e}")


async def notify_success(bot: Bot, group: GroupModel):
    try:
        await bot.send_message(
            chat_id=group.owner_id,
            text=localize_text('messages.pay_success', date=get_displayed_date(group.current_payment_date))
        )
    except Exception as e:
        print(f"Error: {e}")

