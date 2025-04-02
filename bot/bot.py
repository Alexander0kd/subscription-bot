from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.fsm.storage.memory import MemoryStorage

from bot.config import set_bot_commands
from config.settings import TELEGRAM_BOT_TOKEN

from bot.handlers import routers
import asyncio

class TelegramBot:
    def __init__(self):
        self.bot = Bot(
            token=TELEGRAM_BOT_TOKEN,
            default=DefaultBotProperties(parse_mode=ParseMode.HTML),
        )
        self.storage = MemoryStorage()
        self.dp = Dispatcher(storage=self.storage)
        print("Bot inited!")

    async def _setup_middlewares(self):
        """Налаштування middleware"""
        # self.dp.update.middleware.register(DatabaseMiddleware())
        # self.dp.update.middleware.register(UserMiddleware())
        # self.dp.message.middleware.register(ThrottlingMiddleware())
        # self.dp.callback_query.middleware.register(ThrottlingMiddleware())

    async def _register_routers(self):
        """Реєстрація всіх роутерів"""
        for router in routers:
            self.dp.include_router(router)

    async def _on_startup(self):
        """Дії при запуску бота"""
        await set_bot_commands(self.bot)

    async def _on_shutdown(self):
        """Дії при зупинці бота"""
        await self.storage.close()

    async def start(self):
        """Запуск бота"""
        await self._setup_middlewares()
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


def run_bot():
    """Запуск бота з asyncio"""
    bot = TelegramBot()

    try:
        asyncio.run(bot.start())
    except (KeyboardInterrupt, SystemExit):
        print("Bot stopped by user")