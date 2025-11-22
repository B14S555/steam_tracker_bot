from aiogram import Bot, Dispatcher, Router, F
from aiogram.types import Message
from aiogram.filters import Command
from sqlalchemy import select, delete
from db import async_session
from models import UserItem
from steam_api import get_price

router = Router()


@router.message(Command("start"))
async def cmd_start(message: Message):
    text = (
        "Привет! Я бот-трекер цен Steam.\n\n"
        "Команды:\n"
        "/add - добавить предмет для отслеживания\n"
        "/list - список отслеживаемых\n"
        "/remove <id> - удалить предмет\n\n"
        "Формат /add:\n"
        "`/add appid; market_hash_name; target_price`\n"
        "Например:\n"
        "`/add 730; AK-47 | Redline (Field-Tested); 10.50`"
    )
    await message.answer(text, parse_mode="Markdown")


@router.message(Command("add"))
async def cmd_add(message: Message):
    """
    /add 730; AK-47 | Redline (Field-Tested); 10.50
    """
    if not message.text:
        return

    try:
        _, payload = message.text.split(" ", 1)
    except ValueError:
        await message.answer("Нужно указать параметры после /add.")
        return

    parts = [p.strip() for p in payload.split(";")]
    if len(parts) != 3:
        await message.answer("Формат: `/add appid; market_hash_name; target_price`", parse_mode="Markdown")
        return

    appid_str, name, target_str = parts
    try:
        appid = int(appid_str)
        target_price = float(target_str.replace(",", "."))
    except ValueError:
        await message.answer("appid должен быть числом, target_price — числом (пример: 10.50).")
        return

    async with async_session() as session:
        item = UserItem(
            user_id=message.from_user.id,
            appid=appid,
            market_hash_name=name,
            target_price=target_price,
            is_active=True,
        )
        session.add(item)
        await session.commit()
        await session.refresh(item)

    await message.answer(
        f"✅ Добавлен трекинг:\n"
        f"ID: {item.id}\n"
        f"appid: {appid}\n"
        f"name: {name}\n"
        f"target: {target_price}"
    )


@router.message(Command("list"))
async def cmd_list(message: Message):
    async with async_session() as session:
        result = await session.execute(
            select(UserItem).where(UserItem.user_id == message.from_user.id)
        )
        items = result.scalars().all()

    if not items:
        await message.answer("У тебя ещё нет отслеживаемых предметов.")
        return

    lines = ["Твои отслеживаемые предметы:"]
    for it in items:
        status = "✅" if it.is_active else "⏸"
        lines.append(
            f"{status} ID: {it.id} | appid: {it.appid} | target: {it.target_price}\n{it.market_hash_name}"
        )

    await message.answer("\n\n".join(lines))


@router.message(Command("remove"))
async def cmd_remove(message: Message):
    """
    /remove 5
    """
    parts = message.text.split()
    if len(parts) != 2:
        await message.answer("Формат: /remove <id>")
        return

    try:
        item_id = int(parts[1])
    except ValueError:
        await message.answer("ID должен быть числом.")
        return

    async with async_session() as session:
        result = await session.execute(
            select(UserItem).where(
                UserItem.id == item_id,
                UserItem.user_id == message.from_user.id,
            )
        )
        item = result.scalars().first()
        if not item:
            await message.answer("Такой записи не найдено.")
            return

        await session.delete(item)
        await session.commit()

    await message.answer(f"❌ Запись ID {item_id} удалена.")
