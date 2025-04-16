import os
from dotenv import load_dotenv

load_dotenv()

# Global
DEFAULT_LANGUAGE: str = os.getenv("TELEGRAM_DEFAULT_LANGUAGE", "ua")
DAYS_IN_SUBSCRIPTION_MONTH: int = int(os.getenv("DAYS_IN_SUBSCRIPTION_MONTH", 28))

# MongoDB
MONGO_URI: str = os.getenv("MONGO_URI", "mongodb://localhost:27017")
MONGO_DB_NAME: str = os.getenv("MONGO_DB_NAME", "subscription_bot")

# Telegram
TELEGRAM_BOT_TOKEN: str = os.getenv("TELEGRAM_BOT_TOKEN")
DEV_USER_ID: int = int(os.getenv("DEV_USER_ID"))
