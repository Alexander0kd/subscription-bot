from apscheduler.schedulers.asyncio import AsyncIOScheduler
from aiogram import Bot

from bot.chrono.notify_user import notify_success, send_reminders
from db.crud import get_all_groups_by_date
from db.models import GroupModel

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
        if check_group_payments(group):
            if change_date_to_next_payment(group):
                await notify_success(bot, group)
            else:
                print(f"Error with group: f{group}")
        else:
            await send_reminders(bot, group)

    print("Checking finished!")


def check_group_payments(group: GroupModel) -> bool:
    return True


def change_date_to_next_payment(group: GroupModel) -> bool:
    return True
