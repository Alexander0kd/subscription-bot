import os
from dotenv import load_dotenv

load_dotenv()

# Translation
DEFAULT_LANGUAGE: str = os.getenv("TELEGRAM_DEFAULT_LANGUAGE", "ua")

# MongoDB
MONGO_URI = os.getenv("MONGO_URI", "mongodb://localhost:27017")
MONGO_DB_NAME = os.getenv("MONGO_DB_NAME", "subscription_bot")

# Telegram
TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
