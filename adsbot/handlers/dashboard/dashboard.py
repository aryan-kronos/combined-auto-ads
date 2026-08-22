# [Engineered & Developed by Aryan | https://t.me/thatonearyan]
from aiogram import Router, F
from aiogram.types import CallbackQuery

from database.repository.user_repo import UserRepository
from database.repository.dashboard_repo import DashboardRepository
from keyboards.dashboard import dashboard_keyboard
from utils.smart_edit import smart_edit
from custom_emojis import premiumize_text
from config import config

router = Router()


@router.callback_query(F.data == "dashboard")
async def dashboard(callback: CallbackQuery):
    user = await UserRepository.get_user(callback.from_user.id)
    stats = await DashboardRepository.get(user)

    membership = "👑 <b>PREMIUM VIP</b> 💎" if stats["premium"] else "🆓 <b>Standard Free</b>"
    rotation = "🟢 <b>Active & Rotating</b>" if stats["rotation_enabled"] else "🔴 <b>Paused</b>"

    text = f"""
📊 <b>Platform Analytics & Live Dashboard</b>
━━━━━━━━━━━━━━━━━━━━━━━━━━

<blockquote>
👑 <b>Account Tier:</b> {membership}
📱 <b>Accounts:</b> <code>{stats["active_accounts"]} Active</code> / <code>{stats["expired_accounts"]} Expired</code> (Total: <code>{stats["total_accounts"]}/{stats["account_limit"]}</code>)
</blockquote>

<blockquote>
🎯 <b>Active Campaigns:</b> <code>{stats["total_campaigns"]} Total</code>
🟢 <b>Running:</b> <code>{stats["running_campaigns"]}</code> | ⏸ <b>Paused:</b> <code>{stats["stopped_campaigns"]}</code> | ✅ <b>Finished:</b> <code>{stats["completed_campaigns"]}</code>
</blockquote>

<blockquote>
🔄 <b>Auto Bio Rotation:</b> {rotation}
📝 <b>Saved Bios:</b> <code>{stats["saved_bios"]}/5</code>
</blockquote>

<blockquote>
📨 <b>Delivery Analytics:</b>
✅ <b>Messages Delivered:</b> <code>{stats["total_sent"]:,}</code>
❌ <b>Failed / Banned:</b> <code>{stats["failed_sent"]:,}</code>
</blockquote>

{config.BRAND_FOOTER}
"""
    await smart_edit(
        callback,
        text,
        dashboard_keyboard()
    )
