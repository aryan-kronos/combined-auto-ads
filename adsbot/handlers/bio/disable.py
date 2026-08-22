# [Engineered & Developed by Aryan | https://t.me/thatonearyan]
from custom_emojis import button_emoji_id
from aiogram import Router, F
from aiogram.types import CallbackQuery
from aiogram.utils.keyboard import InlineKeyboardBuilder

from database.repository.user_repo import UserRepository
from database.repository.account_repo import AccountRepository
from database.repository.bio_rotation_repo import BioRotationRepository

from utils.smart_edit import smart_edit

router = Router()


@router.callback_query(F.data == "bio_disable")
async def disable_rotation(callback: CallbackQuery):

    user = await UserRepository.get_user(
        callback.from_user.id
    )

    accounts = await AccountRepository.get_accounts(
        user.id
    )

    kb = InlineKeyboardBuilder()

    total = 0

    for account in accounts:

        rotation = await BioRotationRepository.get(
            account.id
        )

        if rotation and rotation.enabled:

            total += 1

            kb.button(
                text=f"🟢 {account.account_name}",
                callback_data=f"bio_disable_{account.id}"
            )

    if total == 0:

        await callback.answer(
            """
❌ No Active Bio Rotation

No Telegram account is
currently using
Auto Bio Rotation.
""",
            show_alert=True
        )
        return

    kb.button(
        text="Back",
        callback_data="bio_home",
        style="danger",
        icon_custom_emoji_id=button_emoji_id("5409284148491726576")
    )

    kb.adjust(1)

    await smart_edit(
        callback,
        f"""
⛔ <b>Disable Auto Bio Rotation</b>
━━━━━━━━━━━━━━━━━━━━━━━━━━

Running Accounts :<b>{total}</b>

━━━━━━━━━━━━━━━━━━━━━━━━━━
Select an account.
""",
        kb.as_markup()
    )


@router.callback_query(
    F.data.startswith("bio_disable_")
)
async def disable_account(callback: CallbackQuery):

    account_id = int(
        callback.data.split("_")[2]
    )

    print("Disabling account:", account_id)

    await BioRotationRepository.disable(
        account_id
    )

    print("Disable finished")

    await callback.answer(
        "✅ Auto Bio Rotation Disabled",
        show_alert=True
    )

    from handlers.bio.menu import bio_home

    await bio_home(callback)