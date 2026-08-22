# [Engineered & Developed by Aryan | https://t.me/thatonearyan]
from aiogram import Router, F
from aiogram.types import CallbackQuery, Message
from aiogram.fsm.context import FSMContext

from states.bio import BioState

from database.repository.user_repo import UserRepository
from database.repository.account_repo import AccountRepository
from database.repository.bio_rotation_repo import (
    BioRotationRepository
)

from keyboards.bio import back_keyboard
from utils.interval_parser import parse_interval
from utils.smart_edit import smart_edit

router = Router()


@router.callback_query(
    F.data == "bio_change_interval"
)
async def ask_interval(
    callback: CallbackQuery,
    state: FSMContext
):

    user = await UserRepository.get_user(
        callback.from_user.id
    )

    accounts = await AccountRepository.get_accounts(
        user.id
    )

    running = False

    for account in accounts:

        rotation = await BioRotationRepository.get(
            account.id
        )

        if rotation and rotation.enabled:

            running = True
            break

    if not running:

        await callback.answer(
            """
❌ No Active Rotation

Enable Auto Bio Rotation
first, then you can
change its interval.
""",
            show_alert=True
        )
        return

    await state.set_state(
        BioState.waiting_custom_interval
    )

    await smart_edit(
        callback,
        """
⏱ <b>Custom Rotation Interval</b>
━━━━━━━━━━━━━━━━━━━━━━━━━━
•Send your new interval.
Examples: 5m ,30m ,2h ,12h ,1d

•Minimum :5 Minutes
•Maximum :30 Days
━━━━━━━━━━━━━━━━━━━━━━━━━━
""",
        back_keyboard()
    )


@router.message(
    BioState.waiting_custom_interval
)
async def save_interval(
    message: Message,
    state: FSMContext
):

    seconds = parse_interval(
        message.text
    )

    if seconds is None:

        await message.answer(
            """
❌ Invalid Interval
 • Examples: 5m ,30m ,2h ,1d
"""
        )
        return

    user = await UserRepository.get_user(
        message.from_user.id
    )

    accounts = await AccountRepository.get_accounts(
        user.id
    )

    updated = 0

    for account in accounts:

        rotation = await BioRotationRepository.get(
            account.id
        )

        if rotation and rotation.enabled:

            rotation.interval = seconds

            await BioRotationRepository.save(
                rotation
            )

            updated += 1

    await state.clear()

    if seconds < 3600:

        interval = f"{seconds // 60} Minutes"

    elif seconds < 86400:

        hours = seconds // 3600

        interval = (
            "1 Hour"
            if hours == 1
            else f"{hours} Hours"
        )

    else:

        days = seconds // 86400

        interval = (
            "1 Day"
            if days == 1
            else f"{days} Days"
        )

    await message.answer(
        f"""
✅ <b>Interval Updated</b>
━━━━━━━━━━━━━━━━━━━━━━━━━━
⏱ New Interval : <b>{interval}</b>
━━━━━━━━━━━━━━━━━━━━━━━━━━
Applied to : <b>{updated}</b>

running account(s).
"""
    )