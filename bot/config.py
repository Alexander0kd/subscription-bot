from translation import *
from aiogram.types import BotCommand
from aiogram import Bot


async def set_bot_commands(bot: Bot):
    """
    Встановлює команди головного меню бота

    Args:
        bot: Екземпляр бота aiogram
    """
    # Список команд з їх описом
    commands = [
        BotCommand(
            command="/start",
            description=localize_text('commands.start')
        ),
        BotCommand(
            command="/join",
            description=localize_text('commands.join')
        ),
    ]

    # Встановлюємо команди
    await bot.set_my_commands(commands)
