# [Engineered & Developed by Aryan | https://t.me/thatonearyan]
from custom_emojis import button_emoji_id
from aiogram import Router, F
from aiogram.types import CallbackQuery
from aiogram.utils.keyboard import InlineKeyboardBuilder

from database.repository.user_repo import UserRepository
from utils.smart_edit import smart_edit
from config import config

router = Router()


@router.callback_query(F.data == "subscription")
@router.callback_query(F.data == "premium")
async def subscription(callback: CallbackQuery):
    user = await UserRepository.get_user(callback.from_user.id)
    kb = InlineKeyboardBuilder()

    if user and user.is_premium:
        kb.button(
            text="Auto Bio Manager",
            callback_data="bio_home",
            style="primary",
            icon_custom_emoji_id=button_emoji_id("5296447931627352804")
        )
        kb.button(
            text="My Accounts",
            callback_data="my_accounts",
            style="primary",
            icon_custom_emoji_id=button_emoji_id("5346136537123801643")
        )
        kb.button(
            text="Home",
            callback_data="home",
            style="danger",
            icon_custom_emoji_id=button_emoji_id("5474534700401833481")
        )
        kb.adjust(2, 1)

        text = f"""
👑 <b>TGBITZ Ads Bot Lifetime VIP</b>
━━━━━━━━━━━━━━━━━━━━━━━━━━

<blockquote>
👤 <b>Account:</b> {callback.from_user.first_name}
🆔 <b>User ID:</b> <code>{callback.from_user.id}</code>
🚦 <b>Status:</b> 👑 <b>Active VIP Member (Lifetime)</b>
</blockquote>

<blockquote expandable>
💎 <b>Your Active VIP Privileges:</b>
• 📱 <b>Multi-Session Power:</b> Up to 10 Telegram accounts enabled
• ⚡ <b>Parallel Campaigns:</b> High-speed concurrent group broadcasting
• 🔁 <b>Custom Looping:</b> Unlimited loop frequency & custom delay timing
• 🔄 <b>Auto Bio Rotation:</b> 5 custom rotating bios active
• 🛡 <b>Clean Identity:</b> Custom branding & default bio removal enabled
• 🛟 <b>Priority 24/7 Support:</b> VIP support routing
</blockquote>

<blockquote>
❤️ <i>Thank you for being a valued VIP member of the {config.NETWORK_NAME}!</i>
</blockquote>

{config.BRAND_FOOTER}
"""

    else:
        kb.button(
            text="Upgrade to VIP (₹499)",
            callback_data="buy_premium",
            style="success",
            icon_custom_emoji_id=button_emoji_id("5262747715552438702")
        )
        kb.button(
            text="Home",
            callback_data="home",
            style="danger",
            icon_custom_emoji_id=button_emoji_id("5474534700401833481")
        )
        kb.adjust(1, 1)

        text = f"""
👑 <b>TGBITZ Ads Bot Lifetime VIP</b>
━━━━━━━━━━━━━━━━━━━━━━━━━━

<blockquote>
👤 <b>Account:</b> {callback.from_user.first_name}
🆔 <b>User ID:</b> <code>{callback.from_user.id}</code>
🚦 <b>Status:</b> 🔴 <b>Standard Free Member</b>
</blockquote>

<blockquote expandable>
💎 <b>Exclusive VIP Privileges Unlocked:</b>
• 📱 <b>Multi-Session Power:</b> Link up to 10 Telegram accounts simultaneously
• ⚡ <b>Parallel Campaigns:</b> Run concurrent ad broadcasts across multiple groups
• 🔁 <b>Custom Looping & Delays:</b> Granular interval controls & automatic retry
• 🔄 <b>Auto Bio Rotation:</b> Store up to 5 rotating bios with scheduled changes
• 🛡 <b>Clean Identity:</b> Completely removes default network tags & attribution
• 🛟 <b>Priority 24/7 Support:</b> Direct expedited escalation with our lead team
• 🎁 <b>Lifetime Access:</b> All future premium features included at no extra cost
</blockquote>

<blockquote>
♾ <b>Plan:</b> Lifetime VIP Membership
💰 <b>Pricing:</b> One-Time Payment (₹499)
</blockquote>

<blockquote>
👉 Tap <b>Upgrade to VIP</b> below to generate payment QR code!
</blockquote>

{config.BRAND_FOOTER}
"""

    await smart_edit(callback, text, kb.as_markup())
