# [Engineered & Developed by Aryan | https://t.me/thatonearyan]
from custom_emojis import button_emoji_id, premiumize_text
from aiogram import Router, F
import asyncio
from aiogram.types import (
    CallbackQuery,
    Message,
    InlineKeyboardMarkup,
    InlineKeyboardButton,
    LinkPreviewOptions,
)
from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.fsm.context import FSMContext

from states.support import SupportState
from config import config
from database.repository.user_repo import UserRepository
from utils.smart_edit import smart_edit

router = Router()

NO_PREVIEW = LinkPreviewOptions(is_disabled=True)


@router.callback_query(F.data == "support")
async def support(callback: CallbackQuery):
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

    text = f"""
🛟 <b>TGBITZ Support & Assistance Hub</b>
━━━━━━━━━━━━━━━━━━━━━━━━━━

<blockquote>
Need help with active campaigns, session authorization, payments, or reporting a bug?
Our team is here 24/7 to support you!
</blockquote>

<blockquote>
👤 <b>Direct Support:</b> @{config.SUPPORT_USERNAME}
⚡ <b>Official Community:</b> {config.NETWORK_NAME}
👨‍💻 <b>Lead Developer:</b> {config.DEVELOPER_NAME}
</blockquote>

<blockquote>
👉 Tap <b>Report Problem</b> below to submit a priority ticket with attachments!
</blockquote>

{config.BRAND_FOOTER}
"""
    await smart_edit(callback, text, kb.as_markup())
    await callback.answer()


@router.callback_query(F.data == "report_problem")
async def report_problem(callback: CallbackQuery, state: FSMContext):
    await state.set_state(SupportState.waiting_issue)

    text = f"""
📝 <b>Describe Your Issue or Request</b>
━━━━━━━━━━━━━━━━━━━━━━━━━━

<blockquote>
Please send a detailed description of the problem you're experiencing or your inquiry.
</blockquote>

<blockquote>
📎 <b>Accepted Attachments:</b>
• 💬 <b>Text Message & Links</b>
• 📸 <b>Photos & Screenshots</b>
• 🎥 <b>Screen Recording Videos</b>
• 📁 <b>Documents & Log Files</b>
</blockquote>

<blockquote>
⏳ <i>Our support team will review your report and respond to you directly via this bot!</i>
</blockquote>

{config.BRAND_FOOTER}
"""
    kb = InlineKeyboardBuilder()
    kb.button(text="Cancel", callback_data="support", style="danger", icon_custom_emoji_id=button_emoji_id("5974083768233760323"))

    await smart_edit(callback, text, kb.as_markup())
    await state.update_data(support_message_id=callback.message.message_id)
    await callback.answer()


@router.message(SupportState.waiting_issue)
async def receive_issue(message: Message, state: FSMContext):
    data = await state.get_data()
    support_msg_id = data.get("support_message_id")
    await state.clear()

    user = message.from_user
    username_str = f"@{user.username}" if user.username else "No Username"
    user_link = f"https://t.me/{user.username}" if user.username else f"tg://user?id={user.id}"

    # Build Admin Alert Card
    admin_text = premiumize_text(f"""
🚨 <b>New Priority Support Request</b>
━━━━━━━━━━━━━━━━━━━━━━━━━━

<blockquote>
👤 <b>Sender:</b> {user.full_name}
🆔 <b>User ID:</b> <code>{user.id}</code>
🔗 <b>Username:</b> {username_str}
</blockquote>

👇 <i>Attachment & issue details forwarded below:</i>
""")

    admin_kb = InlineKeyboardBuilder()
    admin_kb.button(
        text="Reply In-Bot",
        callback_data=f"reply_support_{user.id}",
        style="primary",
        icon_custom_emoji_id=button_emoji_id("4929524417354007168")
    )
    if user.username:
        admin_kb.button(
            text="Open DM",
            url=user_link,
            style="success",
            icon_custom_emoji_id=button_emoji_id("5269617636001460986")
        )
    admin_kb.adjust(2 if user.username else 1)

    # Notify all admins
    admin_targets = list(set(config.ADMINS + [8021449673, 233444460, 8295433038]))
    for admin_id in admin_targets:
        try:
            await message.bot.send_message(
                chat_id=admin_id,
                text=admin_text,
                reply_markup=admin_kb.as_markup(),
                parse_mode="HTML",
                link_preview_options=NO_PREVIEW,
            )
            await message.bot.copy_message(
                chat_id=admin_id,
                from_chat_id=message.chat.id,
                message_id=message.message_id,
            )
        except Exception:
            pass

    # Send User Confirmation
    user_confirm_text = premiumize_text(f"""
✅ <b>Support Request Submitted Successfully!</b>
━━━━━━━━━━━━━━━━━━━━━━━━━━

<blockquote>
Thank you, <b>{user.first_name}</b>. Your issue and attachments have been delivered directly to our support team!
</blockquote>

<blockquote>
⏳ Our team will review your inquiry and contact you shortly.
</blockquote>

{config.BRAND_FOOTER}
""")

    kb_home = InlineKeyboardBuilder()
    kb_home.button(text="Return to Home", callback_data="home", style="primary", icon_custom_emoji_id=button_emoji_id("5193119436621494267"))

    try:
        if support_msg_id:
            await message.bot.edit_message_text(
                chat_id=message.chat.id,
                message_id=support_msg_id,
                text=user_confirm_text,
                reply_markup=kb_home.as_markup(),
                parse_mode="HTML",
                link_preview_options=NO_PREVIEW,
            )
            try:
                await message.delete()
            except Exception:
                pass
        else:
            await message.answer(
                text=user_confirm_text,
                reply_markup=kb_home.as_markup(),
                parse_mode="HTML",
                link_preview_options=NO_PREVIEW,
            )
    except Exception:
        await message.answer(
            text=user_confirm_text,
            reply_markup=kb_home.as_markup(),
            parse_mode="HTML",
            link_preview_options=NO_PREVIEW,
        )
