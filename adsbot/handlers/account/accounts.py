# [Engineered & Developed by Aryan | https://t.me/thatonearyan]
from custom_emojis import button_emoji_id, premiumize_text
from aiogram import Router, F
from aiogram.types import Message, CallbackQuery, LinkPreviewOptions
from aiogram.fsm.context import FSMContext
from aiogram.utils.keyboard import InlineKeyboardBuilder

from states.account import AddAccount
from keyboards.inline import back_keyboard, home_keyboard
from services.sessions.client_manager import client_manager
from database.repository.account_repo import AccountRepository
from database.repository.user_repo import UserRepository
from utils.smart_edit import smart_edit
from services.cache.dashboard_cache import clear
from services.bio.default_bio import apply_default_bio
from config import config

router = Router()
NO_PREVIEW = LinkPreviewOptions(is_disabled=True)


@router.callback_query(F.data == "add_account")
async def add_account(callback: CallbackQuery, state: FSMContext):
    user = await AccountRepository.get_user(callback.from_user.id)
    if not user:
        return await callback.answer("User not found.", show_alert=True)

    accounts = await AccountRepository.get_accounts(user.id)
    limit = 10 if user.is_premium else 1

    if len(accounts) >= limit:
        if user.is_premium:
            await callback.answer(
                "❌ Maximum account limit reached (10 Accounts for VIP).",
                show_alert=True
            )
        else:
            await callback.answer(
                "👑 Premium Required\n\nFree tier allows 1 Telegram session.\nUpgrade to Lifetime Premium to link up to 10 accounts!",
                show_alert=True
            )
        return

    await state.set_state(AddAccount.waiting_phone)

    text = f"""
📱 <b>Link Telegram Account Session</b>
━━━━━━━━━━━━━━━━━━━━━━━━━━

<blockquote>
Please send the <b>phone number</b> of the Telegram account you wish to connect.
</blockquote>

<blockquote>
📞 <b>Format:</b> <code>+1234567890</code> (Include country code)
💡 <i>Ensure you have access to the Telegram app on this number to receive the verification code.</i>
</blockquote>

{config.BRAND_FOOTER}
"""
    kb = InlineKeyboardBuilder()
    kb.button(text="Cancel", callback_data="my_accounts", style="danger", icon_custom_emoji_id=button_emoji_id("5974083768233760323"))
    await smart_edit(callback, text, kb.as_markup())
    await state.update_data(flow_message_id=callback.message.message_id)


@router.message(AddAccount.waiting_phone)
async def get_phone(message: Message, state: FSMContext):
    phone = message.text.strip()
    await message.delete()
    data = await state.get_data()
    flow_id = data.get("flow_message_id")

    text = premiumize_text(f"""
⏳ <b>Connecting to Telegram Server...</b>
━━━━━━━━━━━━━━━━━━━━━━━━━━

<blockquote>
Requesting official authentication code for <code>{phone}</code>...
Please wait a moment.
</blockquote>
""")
    try:
        await message.bot.edit_message_text(
            chat_id=message.chat.id,
            message_id=flow_id,
            text=text,
            parse_mode="HTML",
            link_preview_options=NO_PREVIEW,
        )
    except Exception:
        pass

    await state.update_data(phone=phone)

    await client_manager.send_code(message.from_user.id, phone)
    await state.set_state(AddAccount.waiting_code)

    otp_text = premiumize_text(f"""
📨 <b>Authentication Code Dispatched</b>
━━━━━━━━━━━━━━━━━━━━━━━━━━

<blockquote>
Telegram has sent a verification code to your device (<code>{phone}</code>).
Please enter the code below to complete session authorization.
</blockquote>

<blockquote>
💡 <b>Tip:</b> If the code is formatted like <code>12345</code>, type it directly in chat.
</blockquote>

{config.BRAND_FOOTER}
""")
    kb = InlineKeyboardBuilder()
    kb.button(text="Cancel", callback_data="my_accounts", style="danger", icon_custom_emoji_id=button_emoji_id("5974083768233760323"))

    try:
        await message.bot.edit_message_text(
            chat_id=message.chat.id,
            message_id=flow_id,
            text=otp_text,
            reply_markup=kb.as_markup(),
            parse_mode="HTML",
            link_preview_options=NO_PREVIEW,
        )
    except Exception:
        pass


@router.message(AddAccount.waiting_code)
async def get_code(message: Message, state: FSMContext):
    await message.delete()
    data = await state.get_data()
    flow_id = data.get("flow_message_id")
    phone = data.get("phone")

    verifying_text = premiumize_text("""
⏳ <b>Validating Authorization Code...</b>
━━━━━━━━━━━━━━━━━━━━━━━━━━

<blockquote>
Verifying OTP with Telegram security layer...
</blockquote>
""")
    try:
        await message.bot.edit_message_text(
            chat_id=message.chat.id,
            message_id=flow_id,
            text=verifying_text,
            parse_mode="HTML",
            link_preview_options=NO_PREVIEW,
        )
    except Exception:
        pass

    result = await client_manager.verify_code(
        message.from_user.id,
        phone,
        message.text.strip(),
    )

    if result.get("status") == "wrong_code":
        wrong_text = premiumize_text(f"""
❌ <b>Invalid Verification Code</b>
━━━━━━━━━━━━━━━━━━━━━━━━━━

<blockquote>
The code entered for <code>{phone}</code> is incorrect or has expired.
Please re-enter the valid code from Telegram.
</blockquote>
""")
        kb = InlineKeyboardBuilder()
        kb.button(text="Cancel", callback_data="my_accounts", style="danger", icon_custom_emoji_id=button_emoji_id("5974083768233760323"))
        try:
            await message.bot.edit_message_text(
                chat_id=message.chat.id,
                message_id=flow_id,
                text=wrong_text,
                reply_markup=kb.as_markup(),
                parse_mode="HTML",
                link_preview_options=NO_PREVIEW,
            )
        except Exception:
            pass
        return

    if result.get("status") == "password_required":
        await state.set_state(AddAccount.waiting_password)
        pass_text = premiumize_text(f"""
🔐 <b>Two-Step Verification (2FA) Required</b>
━━━━━━━━━━━━━━━━━━━━━━━━━━

<blockquote>
This Telegram account is protected with a Two-Step Verification password.
Please send your 2FA cloud password to authorize this session.
</blockquote>

{config.BRAND_FOOTER}
""")
        kb = InlineKeyboardBuilder()
        kb.button(text="Cancel", callback_data="my_accounts", style="danger", icon_custom_emoji_id=button_emoji_id("5974083768233760323"))
        try:
            await message.bot.edit_message_text(
                chat_id=message.chat.id,
                message_id=flow_id,
                text=pass_text,
                reply_markup=kb.as_markup(),
                parse_mode="HTML",
                link_preview_options=NO_PREVIEW,
            )
        except Exception:
            pass
        return

    await save_account(message, state, result)


@router.message(AddAccount.waiting_password)
async def get_password(message: Message, state: FSMContext):
    await message.delete()
    data = await state.get_data()
    flow_id = data.get("flow_message_id")

    verifying_pass = premiumize_text("""
⏳ <b>Authenticating 2FA Cloud Password...</b>
━━━━━━━━━━━━━━━━━━━━━━━━━━

<blockquote>
Verifying security credentials with Telegram...
</blockquote>
""")
    try:
        await message.bot.edit_message_text(
            chat_id=message.chat.id,
            message_id=flow_id,
            text=verifying_pass,
            parse_mode="HTML",
            link_preview_options=NO_PREVIEW,
        )
    except Exception:
        pass

    result = await client_manager.verify_password(
        message.from_user.id,
        message.text.strip(),
    )

    if result.get("status") == "wrong_password":
        wrong_p_text = premiumize_text("""
❌ <b>Incorrect 2FA Password</b>
━━━━━━━━━━━━━━━━━━━━━━━━━━

<blockquote>
The Two-Step Verification password you entered is incorrect.
Please re-enter your valid password.
</blockquote>
""")
        kb = InlineKeyboardBuilder()
        kb.button(text="Cancel", callback_data="my_accounts", style="danger", icon_custom_emoji_id=button_emoji_id("5974083768233760323"))
        try:
            await message.bot.edit_message_text(
                chat_id=message.chat.id,
                message_id=flow_id,
                text=wrong_p_text,
                reply_markup=kb.as_markup(),
                parse_mode="HTML",
                link_preview_options=NO_PREVIEW,
            )
        except Exception:
            pass
        return

    await save_account(message, state, result)


async def save_account(message: Message, state: FSMContext, result: dict):
    data = await state.get_data()
    flow_id = data.get("flow_message_id")
    phone = data.get("phone")
    await state.clear()

    user = await AccountRepository.get_user(message.from_user.id)
    account_name = result.get("account_name") or f"Account {phone[-4:]}"
    session_string = result.get("session_string")

    account = await AccountRepository.add_account(
        user_id=user.id,
        account_name=account_name,
        phone=phone,
        session_string=session_string,
    )

    try:
        await apply_default_bio(session_string)
    except Exception:
        pass

    clear(user.id)

    success_text = premiumize_text(f"""
✅ <b>Telegram Account Linked Successfully!</b>
━━━━━━━━━━━━━━━━━━━━━━━━━━

<blockquote>
👤 <b>Account Name:</b> {account_name}
📞 <b>Phone Number:</b> <code>{phone}</code>
🛡 <b>Session Status:</b> 🟢 <b>Active & Ready</b>
</blockquote>

<blockquote>
🎉 You can now use this session for automated group advertising and scheduled Auto Bio rotation!
</blockquote>

{config.BRAND_FOOTER}
""")

    kb = InlineKeyboardBuilder()
    kb.button(text="My Accounts", callback_data="my_accounts", style="primary", icon_custom_emoji_id=button_emoji_id("5346136537123801643"))
    kb.button(text="Create Campaign", callback_data="create_campaign", style="success", icon_custom_emoji_id=button_emoji_id("5389057356493511934"))
    kb.button(text="Home", callback_data="home", style="primary", icon_custom_emoji_id=button_emoji_id("5193119436621494267"))
    kb.adjust(2, 1)

    try:
        await message.bot.edit_message_text(
            chat_id=message.chat.id,
            message_id=flow_id,
            text=success_text,
            reply_markup=kb.as_markup(),
            parse_mode="HTML",
            link_preview_options=NO_PREVIEW,
        )
    except Exception:
        await message.answer(
            text=success_text,
            reply_markup=kb.as_markup(),
            parse_mode="HTML",
            link_preview_options=NO_PREVIEW,
        )
