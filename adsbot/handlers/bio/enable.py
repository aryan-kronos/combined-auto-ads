# [Engineered & Developed by Aryan | https://t.me/thatonearyan]
from custom_emojis import button_emoji_id
from aiogram import Router, F
from aiogram.types import CallbackQuery
from aiogram.utils.keyboard import InlineKeyboardBuilder

from database.repository.user_repo import UserRepository
from database.repository.account_repo import AccountRepository
from database.repository.bio_repo import BioRepository
from database.repository.bio_rotation_repo import BioRotationRepository

from services.sessions.session_checker import check_session

from keyboards.bio import (
    no_account_keyboard,
    minimum_bio_keyboard
)

from utils.smart_edit import smart_edit

router = Router()


@router.callback_query(F.data == "bio_enable")
async def enable_bio(callback: CallbackQuery):

    user = await UserRepository.get_user(
        callback.from_user.id
    )

    bios = await BioRepository.get_bios(
        user.id
    )

    # Minimum 2 bios required
    if len(bios) < 2:

        await smart_edit(
            callback,
            f"""
⚠ <b>Minimum 2 Bios Required</b>
━━━━━━━━━━━━━━━━━━━━━━━━━━
You currently have :<b>{len(bios)}</b> saved bio(s).

•Auto Bio Rotation requires
at least <b>2 bios</b>.
•Please add another bio
to continue.
━━━━━━━━━━━━━━━━━━━━━━━━━━
""",
            minimum_bio_keyboard()
        )

        return

    await callback.answer(
        """
⏳ Please Wait

Checking your active
Telegram accounts...

This usually takes
1–3 seconds.
""",
        show_alert=True
    )

    accounts = await AccountRepository.get_accounts(
        user.id
    )

    valid_accounts = []

    for account in accounts:

        try:

            alive = await check_session(
                account.session_string
            )

        except Exception:

            alive = False

        await AccountRepository.update_status(
            account.id,
            alive
        )

        if alive:
            valid_accounts.append(account)

    if not valid_accounts:

        await callback.answer(
            """
❌ NO ACTIVE ACCOUNT

No active Telegram account
was found.
""",
            show_alert=True
        )

        await smart_edit(
            callback,
            """
❌ <b>No Active Account</b>
━━━━━━━━━━━━━━━━━━━━━━━━━━
No active Telegram account
is available.

Possible reasons:
• No account has been added.
• All Telegram sessions
have expired.
━━━━━━━━━━━━━━━━━━━━━━━━━━

Please add a Telegram
account to continue.
""",
            no_account_keyboard()
        )

        return

    kb = InlineKeyboardBuilder()

    for account in valid_accounts:

        rotation = await BioRotationRepository.get(
            account.id
        )

        enabled = (
            rotation is not None
            and rotation.enabled
        )

        kb.button(
            text=(
                f"🟢 {account.account_name} ✓"
                if enabled
                else f"⚪ {account.account_name}",
            ),
            callback_data=f"bio_account_{account.id}",
             style="primary"
        )

    kb.button(
        text="Back",
        callback_data="bio_home",
        style="danger",
        icon_custom_emoji_id=button_emoji_id("5409284148491726576")
    )

    kb.adjust(1)

    await smart_edit(
        callback,
        """
📱 <b>Select Telegram Account</b>
━━━━━━━━━━━━━━━━━━━━━━━━━━
•Choose the account you want to use for
Auto Bio Rotation.

🟢 = Already Enabled
⚪ = Available
━━━━━━━━━━━━━━━━━━━━━━━━━━
""",
        kb.as_markup()
    )