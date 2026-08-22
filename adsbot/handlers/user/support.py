# [Engineered & Developed by Aryan | https://t.me/thatonearyan]
from aiogram import Router, F
from aiogram.types import CallbackQuery
from aiogram.utils.keyboard import InlineKeyboardBuilder
from utils.smart_edit import smart_edit
from custom_emojis import button_emoji_id, premiumize_text
from config import config

router = Router()


@router.callback_query(F.data == "support")
async def support_handler(callback: CallbackQuery):
    text = f"""
🛟 <b>Customer Support & Assistance</b>
━━━━━━━━━━━━━━━━━━━━━━━━━━

<blockquote>
Need help adding Telegram sessions, launching campaigns, or setting up Auto Bio rotation?
Our dedicated support team is available 24/7!
</blockquote>

<blockquote>
👤 <b>Support Lead:</b> <a href='{config.SUPPORT_URL}'>@{config.SUPPORT_USERNAME}</a>
⚡ <b>Official Community:</b> <a href='{config.NETWORK_URL}'>{config.NETWORK_NAME}</a>
👨‍💻 <b>Lead Developer:</b> <a href='{config.DEVELOPER_URL}'>{config.DEVELOPER_NAME}</a>
</blockquote>

{config.BRAND_FOOTER}
"""
    kb = InlineKeyboardBuilder()
    kb.button(
        text="Contact Support",
        url=config.SUPPORT_URL,
        style="primary",
        icon_custom_emoji_id=button_emoji_id("5866185084427572234")
    )
    kb.button(
        text="Contact Lead",
        url=config.DEVELOPER_URL,
        style="success",
        icon_custom_emoji_id=button_emoji_id("5269617636001460986")
    )
    kb.button(
        text="Report Problem",
        callback_data="report_problem",
        style="primary",
        icon_custom_emoji_id=button_emoji_id("4929524417354007168")
    )
    kb.button(
        text="Home",
        callback_data="home",
        style="danger",
        icon_custom_emoji_id=button_emoji_id("5474534700401833481")
    )
    kb.adjust(2, 1, 1)

    await smart_edit(callback, text, reply_markup=kb.as_markup())
