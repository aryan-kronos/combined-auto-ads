# [Engineered & Developed by Aryan | https://t.me/thatonearyan]
from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message
from loader import bot
from config import config
from database.session import db

router = Router()

@router.message(Command("broadcast"))
async def broadcast(message: Message):
    if message.from_user.id not in config.ADMINS:
        return
    if not message.reply_to_message:
        await message.answer("Reply to any message with /broadcast")
        return

    users = [d["telegram_id"] async for d in db.users.find({}, {"telegram_id": 1})]
    sent = failed = 0
    status = await message.answer(f"📢 Broadcasting...\n\n0/{len(users)}")

    for i, user_id in enumerate(users, start=1):
        try:
            await bot.copy_message(chat_id=user_id, from_chat_id=message.chat.id,
                                   message_id=message.reply_to_message.message_id)
            sent += 1
        except Exception:
            failed += 1
        if i % 20 == 0 or i == len(users):
            try:
                await status.edit_text(f"📢 Broadcasting...\n\nProgress: {i}/{len(users)}\n\n✅ Sent : {sent}\n❌ Failed : {failed}")
            except Exception:
                pass

    await status.edit_text(f"✅ Broadcast Completed\n\n👥 Total Users : {len(users)}\n\n📤 Sent : {sent}\n\n❌ Failed : {failed}")
