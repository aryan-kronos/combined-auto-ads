# [Engineered & Developed by Aryan | https://t.me/thatonearyan]
from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message
from config import config
from database.session import db

router = Router()

@router.message(Command("status"))
async def bot_status(message: Message):
    if message.from_user.id not in config.ADMINS:
        return

    total_users = await db.users.count_documents({})
    premium_users = await db.users.count_documents({"is_premium": True})
    banned_users = await db.users.count_documents({"is_banned": True})
    total_accounts = await db.accounts.count_documents({})
    active_accounts = await db.accounts.count_documents({"active": True})
    total_campaigns = await db.campaigns.count_documents({})
    running_campaigns = await db.campaigns.count_documents({"running": True})
    paused_campaigns = await db.campaigns.count_documents({"paused": True})
    completed_campaigns = await db.campaigns.count_documents({"completed": True})

    total_sent = 0
    total_failed = 0
    async for d in db.campaigns.find({}, {"total_sent": 1, "failed_sent": 1}):
        total_sent += int(d.get("total_sent", 0) or 0)
        total_failed += int(d.get("failed_sent", 0) or 0)

    await message.answer(f"""
📊 <b>TGBITZ ADS BOT STATUS</b>

━━━━━━━━━━━━━━

👥 Users : <b>{total_users}</b>
💎 Premium : <b>{premium_users}</b>
🚫 Banned : <b>{banned_users}</b>

━━━━━━━━━━━━━━

📱 Accounts : <b>{total_accounts}</b>
🟢 Active : <b>{active_accounts}</b>
🔴 Dead : <b>{total_accounts - active_accounts}</b>

━━━━━━━━━━━━━━

📢 Campaigns : <b>{total_campaigns}</b>
🟢 Running : <b>{running_campaigns}</b>
⏸ Paused : <b>{paused_campaigns}</b>
✅ Completed : <b>{completed_campaigns}</b>

━━━━━━━━━━━━━━

📤 Messages Sent : <b>{total_sent}</b>
❌ Failed : <b>{total_failed}</b>
""")
