import os
from dotenv import load_dotenv

load_dotenv()

BOT_TOKEN = os.getenv("8259194269:AAHBCAko3MzMHuzCrhbCl26vlA74wl16hXs")

# Хост, под которым Fly.io будет доступен, например:
# https://steam-tracker-bot.fly.dev
WEBHOOK_HOST = os.getenv("FLY_APP_HOST")  # ОБЯЗАТЕЛЬНО задать в переменных окружения
WEBHOOK_PATH = f"/webhook/{BOT_TOKEN}" if BOT_TOKEN else "/webhook"
WEBHOOK_URL = f"{WEBHOOK_HOST}{WEBHOOK_PATH}" if WEBHOOK_HOST and BOT_TOKEN else None

# База: локально и на Fly
if os.getenv("FLY_APP_NAME"):
    DATABASE_URL = "sqlite+aiosqlite:////data/database.db"
else:
    DATABASE_URL = "sqlite+aiosqlite:///database.db"
