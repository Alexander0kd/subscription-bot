from translation import *
from aiogram.types import BotCommand
from aiogram import Bot


async def set_bot_commands(bot: Bot):
    commands = [
        BotCommand(
            command="/start",
            description=localize_text('commands.start.title')
        ),
        BotCommand(
            command="/join",
            description=localize_text('commands.join.title')
        ),
    ]

    await bot.set_my_commands(commands)
