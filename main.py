import asyncio
from aiohttp import web
from aiogram import Bot, Dispatcher
from aiogram.webhook.aiohttp_server import SimpleRequestHandler, setup_application

from config import BOT_TOKEN, WEBHOOK_URL, WEBHOOK_PATH
from bot import router
from db import init_db
from watcher import price_watcher  # см. ниже, мы вынесем функцию в watcher.py


async def on_startup(app: web.Application):
    if not BOT_TOKEN:
        raise RuntimeError("8259194269:AAHBCAko3MzMHuzCrhbCl26vlA74wl16hXs")
    if not WEBHOOK_URL:
        raise RuntimeError("Не задан WEBHOOK_HOST (FLY_APP_HOST) или BOT_TOKEN!")

    app["bot"] = Bot(BOT_TOKEN, parse_mode="HTML")
    dp = Dispatcher()
    dp.include_router(router)

    app["dp"] = dp

    await init_db()
    await app["bot"].set_webhook(WEBHOOK_URL)
    print("✅ Webhook установлен:", WEBHOOK_URL)

    # Запускаем фонового вотчера
    app["watcher_task"] = asyncio.create_task(price_watcher(app["bot"]))

    # Регистрируем обработчик вебхука
    SimpleRequestHandler(
        dispatcher=dp,
        bot=app["bot"],
    ).register(app, path=WEBHOOK_PATH)


async def on_shutdown(app: web.Application):
    await app["bot"].delete_webhook()
    await app["bot"].session.close()
    if "watcher_task" in app:
        app["watcher_task"].cancel()


def create_app() -> web.Application:
    app = web.Application()
    app.on_startup.append(on_startup)
    app.on_shutdown.append(on_shutdown)
    setup_application(app, app["dp"] if "dp" in app else None)
    return app


if __name__ == "__main__":
    web.run_app(create_app(), host="0.0.0.0", port=8080)
