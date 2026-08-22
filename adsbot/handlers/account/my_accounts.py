# [Engineered & Developed by Aryan | https://t.me/thatonearyan]
from custom_emojis import button_emoji_id, premiumize_text
import asyncio

from aiogram import Router, F
from aiogram.types import CallbackQuery
from aiogram.utils.keyboard import InlineKeyboardBuilder

from database.repository.account_repo import AccountRepository
from keyboards.account import (
    accounts_keyboard,
    account_details_keyboard
)
from utils.smart_edit import smart_edit
from services.cache.dashboard_cache import clear
from services.sessions.session_checker import check_session
from config import config

router = Router()


@router.callback_query(F.data == "my_accounts")
async def my_accounts(callback: CallbackQuery):
    user = await AccountRepository.get_user(callback.from_user.id)
    if not user:
        return await callback.answer("User not found.", show_alert=True)

    accounts = await AccountRepository.get_accounts(user.id)

    if not accounts:
        kb = InlineKeyboardBuilder()
        kb.button(
            text="Add Account",
            callback_data="add_account",
            style="success",
            icon_custom_emoji_id=button_emoji_id("5287354223141342798")
        )
        kb.button(
            text="Home",
            callback_data="home",
            style="danger",
            icon_custom_emoji_id=button_emoji_id("5474534700401833481")
        )
        kb.adjust(1, 1)

        text = f"""
📱 <b>My Telegram Accounts</b>
━━━━━━━━━━━━━━━━━━━━━━━━━━

<blockquote>
❌ <b>No Telegram Accounts Linked!</b>
You haven't connected any Telegram user sessions to this bot yet.
</blockquote>

<blockquote>
👉 Tap <b>Add Account</b> below to link your sessions for automated broadcasting & bio rotation!
</blockquote>

{config.BRAND_FOOTER}
"""
        await smart_edit(callback, text, kb.as_markup())
        return

    active = 0
    lines = []
    for acc in accounts:
        try:
            status = await check_session(acc.session_string)
            await AccountRepository.update_status(acc.id, status)
            acc.active = status
        except Exception:
            status = False

        if status:
            active += 1
            badge = "🟢 Active"
        else:
            badge = "🔴 Expired"

        lines.append(f"• 👤 <b>{acc.account_name}</b> (<code>{acc.phone}</code>) — {badge}")

    acc_list_str = "\n".join(lines)
    text = f"""
📱 <b>My Telegram Accounts</b>
━━━━━━━━━━━━━━━━━━━━━━━━━━

<blockquote>
📊 <b>Total Linked Sessions:</b> <code>{len(accounts)}</code>
🟢 <b>Active:</b> <code>{active}</code> | 🔴 <b>Expired:</b> <code>{len(accounts)-active}</code>
</blockquote>

<blockquote>
{acc_list_str}
</blockquote>

<blockquote>
👇 <b>Tap an account below to view details or manage session:</b>
</blockquote>

{config.BRAND_FOOTER}
"""
    await smart_edit(callback, text, accounts_keyboard(accounts))


@router.callback_query(F.data.startswith("account_"))
async def account_details(callback: CallbackQuery):
    account_id = int(callback.data.split("_")[1])
    account = await AccountRepository.get_account(account_id)

    if not account:
        return await callback.answer("Account not found.", show_alert=True)

    status = await check_session(account.session_string)
    status_str = "🟢 <b>Active & Ready</b>" if status else "🔴 <b>Session Expired / Logged Out</b>"

    text = f"""
📱 <b>Telegram Account Profile</b>
━━━━━━━━━━━━━━━━━━━━━━━━━━

<blockquote>
👤 <b>Account Name:</b> {account.account_name}
📞 <b>Phone Number:</b> <code>{account.phone}</code>
🚦 <b>Status:</b> {status_str}
📅 <b>Linked Date:</b> <code>{account.created_at.strftime("%d %b %Y, %H:%M")}</code>
</blockquote>

{config.BRAND_FOOTER}
"""
    await smart_edit(callback, text, account_details_keyboard(account.id))
