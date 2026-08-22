# [Engineered & Developed by Aryan | https://t.me/thatonearyan]
from aiogram import Router, F
from aiogram.types import CallbackQuery

from database.repository.user_repo import UserRepository
from database.repository.bio_repo import BioRepository
from database.repository.bio_rotation_repo import BioRotationRepository
from database.repository.account_repo import AccountRepository

from keyboards.bio import bio_home_keyboard

from utils.smart_edit import smart_edit
from config import config

router = Router()


@router.callback_query(F.data == "bio_home")
async def bio_home(callback: CallbackQuery):

    user = await UserRepository.get_user(
        callback.from_user.id
    )

    if not user:

        await callback.answer(
            "User not found.",
            show_alert=True
        )
        return

    if not user.is_premium:

        await callback.answer(
            """
🔒 PREMIUM FEATURE
• availableonly for Premium Members.
✨ Features :
• Store up to 5 Bios
• Automatic Bio Rotation
""",
            show_alert=True
        )
        return

    bios = await BioRepository.get_bios(
        user.id
    )

    accounts = await AccountRepository.get_accounts(
        user.id
    )

    running = 0
    current_interval = "Not Set"

    for account in accounts:

        rotation = await BioRotationRepository.get(
            account.id
        )

        if rotation and rotation.enabled:

            running += 1

            seconds = rotation.interval

            if seconds < 3600:

                current_interval = (
                    f"{seconds // 60} Minutes"
                )

            elif seconds < 86400:

                hours = seconds // 3600

                current_interval = (
                    "1 Hour"
                    if hours == 1
                    else f"{hours} Hours"
                )

            else:

                days = seconds // 86400

                current_interval = (
                    "1 Day"
                    if days == 1
                    else f"{days} Days"
                )

    available = len(accounts) - running

    await smart_edit(
        callback,
        f"""
🔄 <b>Auto Profile Bio Rotation Manager</b>
━━━━━━━━━━━━━━━━━━━━━━━━━━

<blockquote>
📝 <b>Saved Bios:</b> <code>{len(bios)} / 5</code>
🟢 <b>Active Rotations:</b> <code>{running}</code>
📱 <b>Available Accounts:</b> <code>{available}</code>
⏱ <b>Rotation Interval:</b> <code>{current_interval}</code>
</blockquote>

<blockquote>
👉 Rotate custom bio texts across all your connected Telegram accounts automatically 24/7!
</blockquote>

{config.BRAND_FOOTER}
""",
        bio_home_keyboard()
    )

    await callback.answer()