# [Engineered & Developed by Aryan | https://t.me/thatonearyan]
from aiogram import Router, F
from aiogram.types import CallbackQuery
from aiogram.utils.keyboard import InlineKeyboardBuilder
from utils.smart_edit import smart_edit
from custom_emojis import button_emoji_id, premiumize_text
from config import config

router = Router()


@router.callback_query(F.data == "guide")
async def guide(callback: CallbackQuery):
    text = f"""
📖 <b>How to Use {config.BOT_NAME}</b>
━━━━━━━━━━━━━━━━━━━━━━━━━━

<blockquote>
1️⃣ <b>Step 1: Link Your Telegram Accounts</b> 📱
• Tap <b>Add Account</b> on the home screen.
• Send your session string or phone number to authenticate.
• Add up to 5 accounts (Unlimited with 👑 Premium VIP).
</blockquote>

<blockquote>
2️⃣ <b>Step 2: Create Your Advertising Campaign</b> 📢
• Tap <b>Create Campaign</b>.
• Send your promotional message (text, photos, media, links).
• Select target public/private groups for automated broadcasts.
</blockquote>

<blockquote>
3️⃣ <b>Step 3: Setup Automated Bio Rotation</b> 🔄
• Tap <b>Auto Bio</b> from the main menu.
• Save up to 5 advertising bios and set your rotation timer.
• Your accounts will automatically rotate their profiles 24/7!
</blockquote>

<blockquote>
4️⃣ <b>Step 4: Launch & Monitor Live Analytics</b> 🚀
• Tap <b>Dashboard</b> to track sent messages, active sessions, and broadcast health in real-time!
</blockquote>

{config.BRAND_FOOTER}
"""
    kb = InlineKeyboardBuilder()
    kb.button(text="Developer (Aryan)", url=config.DEVELOPER_URL, style="success", icon_custom_emoji_id=button_emoji_id("5269617636001460986"))
    kb.button(text="Home", callback_data="home", style="danger", icon_custom_emoji_id=button_emoji_id("5474534700401833481"))
    kb.adjust(1, 1)

    await smart_edit(callback, text, reply_markup=kb.as_markup())
