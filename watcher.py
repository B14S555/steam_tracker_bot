from aiogram import Bot
import asyncio
from sqlalchemy import select
from db import async_session
from models import UserItem
from steam_api import get_price

CHECK_INTERVAL = 300  # 5 минут


async def price_watcher(bot: Bot):
    while True:
        try:
            async with async_session() as session:
                result = await session.execute(
                    select(UserItem).where(UserItem.is_active == True)
                )
                items = result.scalars().all()

            for item in items:
                low, median = get_price(item.appid, item.market_hash_name)
                if not low:
                    continue

                def parse_price(p: str) -> float:
                    p = p.replace("$", "").replace("USD", "").strip()
                    p = p.replace(",", ".")
                    try:
                        return float(p)
                    except ValueError:
                        return 999999.0

                low_val = parse_price(low)
                if low_val <= item.target_price:
                    text = (
                        f"🔥 Цена упала!\n\n"
                        f"{item.market_hash_name}\n"
                        f"appid: {item.appid}\n"
                        f"Текущая низшая цена: {low} (≈{low_val})\n"
                        f"Твоя целевая: {item.target_price}\n\n"
                        f"Открыть в Steam:\n"
                        f"https://steamcommunity.com/market/listings/{item.appid}/"
                        f"{item.market_hash_name.replace(' ', '%20')}"
                    )
                    try:
                        await bot.send_message(item.user_id, text)
                    except Exception as e:
                        print("Send message error:", e)

            await asyncio.sleep(CHECK_INTERVAL)
        except Exception as e:
            print("Watcher error:", e)
            await asyncio.sleep(10)
