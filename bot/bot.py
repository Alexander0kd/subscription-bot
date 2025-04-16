from config import TELEGRAM_BOT_TOKEN

import asyncio
from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.fsm.storage.memory import MemoryStorage

from apscheduler.schedulers.asyncio import AsyncIOScheduler

from .chrono import setup_scheduler
from .config import set_bot_commands
from .handlers import routers as handler_routers
from .services import routers as handler_services

class TelegramBot:
    def __init__(self):
        self.bot = Bot(
            token=TELEGRAM_BOT_TOKEN,
            default=DefaultBotProperties(parse_mode=ParseMode.HTML),
        )
        self.storage = MemoryStorage()
        self.dp = Dispatcher(storage=self.storage)
        self.scheduler = AsyncIOScheduler()
        print("Bot inited!")

    async def _register_routers(self):
        for router in handler_routers:
            self.dp.include_router(router)
        for router in handler_services:
            self.dp.include_router(router)

    async def _on_startup(self):
        await set_bot_commands(self.bot)
        await setup_scheduler(self.bot, self.scheduler)
        self.scheduler.start()

    async def _on_shutdown(self):
        await self.storage.close()
        self.scheduler.shutdown()

    async def start(self):
        await self._register_routers()

        self.dp.startup.register(self._on_startup)
        self.dp.shutdown.register(self._on_shutdown)

        try:
            print("Bot started!")
            await self.dp.start_polling(
                self.bot,
                allowed_updates=self.dp.resolve_used_update_types()
            )
        finally:
            await self._on_shutdown()


bot = TelegramBot()


def run_bot():
    try:
        asyncio.run(bot.start())
    except (KeyboardInterrupt, SystemExit):
        print("Bot stopped by user")
