# [Engineered & Developed by Aryan | https://t.me/thatonearyan]
from aiogram import Router, F
from aiogram.types import CallbackQuery
from aiogram.utils.keyboard import InlineKeyboardBuilder
from custom_emojis import button_emoji_id, premiumize_text
import ui

from config import (
    REFERRAL_REWARD,
    BOT_USERNAME,
    BOT_NAME_STYLED,
    BRAND_FOOTER,
    DEVELOPER_URL,
)
from database import get_balance
from utils import edit_or_send

router = Router()


def referral_share_keyboard(user_id: int):
    kb = InlineKeyboardBuilder()
    ref_link = f"https://t.me/{BOT_USERNAME}?start={user_id}"
    share_url = f"https://t.me/share/url?url={ref_link}&text=🚀%20Boost%20your%20Telegram%20Channel%20with%20instant%20Views%20and%20Reactions%20on%20{BOT_USERNAME}!"

    kb.button(
        text="Share Referral Link",
        url=share_url,
        style="primary",
        icon_custom_emoji_id=button_emoji_id("4929524417354007168")
    )
    kb.button(
        text="Developer (Aryan)",
        url=DEVELOPER_URL,
        style="success",
        icon_custom_emoji_id=button_emoji_id("5269617636001460986")
    )
    kb.button(
        text="Back",
        callback_data="home",
        style="danger",
        icon_custom_emoji_id=button_emoji_id("5409284148491726576")
    )
    kb.adjust(1, 1, 1)
    return kb.as_markup()


@router.callback_query(F.data == "refer")
async def referral(call: CallbackQuery):
    balance = await get_balance(call.from_user.id)
    link = f"https://t.me/{BOT_USERNAME}?start={call.from_user.id}"

    text = f"""
🎁 <b>Refer & Earn Free Credits</b>
━━━━━━━━━━━━━━━━━━━━━━━━━━

<blockquote>
Invite channel owners, admins, and friends to <b>{BOT_NAME_STYLED}</b> and earn free credits every time someone joins!
</blockquote>

<blockquote>
🎉 <b>Your Commission:</b> <code>+{REFERRAL_REWARD} Credits</code> per friend
🎁 <b>Friend Bonus:</b> <code>+{REFERRAL_REWARD} Credits</code> on joining
💰 <b>Your Current Balance:</b> <code>{balance:,} Credits</code>
</blockquote>

<blockquote>
🔗 <b>Your Exclusive Referral Link:</b>
<code>{link}</code>
<i>(Tap link above to copy)</i>
</blockquote>

"""
    await edit_or_send(
        call,
        text,
        referral_share_keyboard(call.from_user.id),
    )
    await call.answer()
