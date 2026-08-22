# [Engineered & Developed by Aryan | https://t.me/thatonearyan]
from aiogram import Router, F
from aiogram.types import CallbackQuery
from aiogram.utils.keyboard import InlineKeyboardBuilder
from utils.smart_edit import smart_edit
from custom_emojis import button_emoji_id, premiumize_text
from config import config

router = Router()


@router.callback_query(F.data == "buy_tg_acc")
async def buy_accounts_menu(callback: CallbackQuery):
    text = f"""
🛒 <b>Purchase Verified Telegram Accounts</b>
━━━━━━━━━━━━━━━━━━━━━━━━━━

<blockquote>
Get high-trust, aged Telegram sessions ready for instant broadcasting & bio rotation:
• 📱 <b>Indian / US / Global Numbers</b>
• 🛡 <b>2FA Enabled & Anti-Ban Configured</b>
• ⚡ <b>Instant Delivery via Session File</b>
</blockquote>

<blockquote>
👉 Contact our verified account vendor directly:
</blockquote>

{config.BRAND_FOOTER}
"""
    kb = InlineKeyboardBuilder()
    kb.button(text="Buy Verified Accounts", url=config.SUPPORT_URL, style="success", icon_custom_emoji_id=button_emoji_id("6296218646284863141"))
    kb.button(text="Developer (Aryan)", url=config.DEVELOPER_URL, style="success", icon_custom_emoji_id=button_emoji_id("5269617636001460986"))
    kb.button(text="Home", callback_data="home", style="danger", icon_custom_emoji_id=button_emoji_id("5474534700401833481"))
    kb.adjust(1, 1, 1)

    await smart_edit(callback, text, reply_markup=kb.as_markup())
