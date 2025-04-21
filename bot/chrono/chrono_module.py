from datetime import datetime, timedelta

from apscheduler.schedulers.asyncio import AsyncIOScheduler
from aiogram import Bot

from bot.chrono.notify_user import notify_success, send_reminders
from config.settings import DAYS_IN_SUBSCRIPTION_MONTH
from db.crud import get_all_groups_by_date
from db.crud.group_crud import update_group
from db.models import GroupModel, PaymentPeriod, PaymentMethod, PaymentStatus, MemberModel


async def setup_scheduler(bot: Bot, scheduler: AsyncIOScheduler):
    scheduler.add_job(
        daily_payment_check,
        'cron',
        hour=0,
        minute=0,
        kwargs={'bot': bot},
        timezone='Europe/Kiev'
    )


async def daily_payment_check(bot: Bot):
    groups = await get_all_groups_by_date()
    print(f"Checking [{len(groups)}] groups!")

    for group in groups:
        print(group)
        if await check_group_payments(group):
            if await change_date_to_next_payment(group):
                await notify_success(bot.bot, group)
            else:
                print(f"Error with group: f{group}")
        else:
            await send_reminders(bot.bot, group)

    print("Checking finished!")


async def check_group_payments(group: GroupModel) -> bool:
    for member in group.members:
        if group.should_user_pay(member):
            return False

    if get_group_latest_payment_date(group) > datetime.now():
        return False

    return True


async def change_date_to_next_payment(group: GroupModel) -> bool:
    try:
        max_date = get_group_latest_payment_date(group)
        time_delta = get_group_delta(group)

        members = group.members
        for member in members:
            member.status = PaymentStatus.UNPAID

        group.members = members
        group.current_payment_date = max_date + time_delta
        await update_group(group)

        return True
    except Exception as e:
        print(f"Error: {e}")
        return False


def get_group_delta(group: GroupModel) -> timedelta:
    if group.payment_period == PaymentPeriod.WEEKLY:
        return timedelta(weeks=1)

    if group.payment_period == PaymentPeriod.MONTHLY:
         return timedelta(days=DAYS_IN_SUBSCRIPTION_MONTH)

    return timedelta(days=1)


def get_group_latest_payment_date(group: GroupModel) -> datetime:
    max_date = datetime.now()

    for member in group.members:
        date = group.get_next_payment_date(member)
        if date > max_date:
            max_date = date

    return max_date