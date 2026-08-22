# [Engineered & Developed by Aryan | https://t.me/thatonearyan]
from datetime import datetime

from aiogram import Router, F
from aiogram.types import CallbackQuery
from aiogram.fsm.context import FSMContext

from database.repository.bio_rotation_repo import (
    BioRotationRepository
)

from database.repository.bio_rotation_item_repo import (
    BioRotationItemRepository
)

from database.repository.account_repo import (
    AccountRepository
)

from database.repository.bio_repo import (
    BioRepository
)

from services.bio.set_bio import (
    set_bio
)

from keyboards.bio import bio_home_keyboard

from utils.smart_edit import smart_edit

router = Router()


@router.callback_query(
    F.data == "bio_enable_confirm"
)
async def enable_rotation(
    callback: CallbackQuery,
    state: FSMContext
):

    data = await state.get_data()

    account_id = data.get(
        "account_id"
    )

    bios = data.get(
        "selected_bios",
        []
    )

    interval = data.get(
        "interval",
        3600
    )

    rotation = await BioRotationRepository.create(
        account_id=account_id,
        interval=interval
    )

    # Remove previous selected bios
    await BioRotationItemRepository.clear(
        rotation.id
    )

    # Save new selected bios
    for bio in bios:

        await BioRotationItemRepository.add(
            rotation.id,
            bio
        )

    # Apply first bio instantly
    if bios:

        account = await AccountRepository.get_account(
            account_id
        )

        first_bio = await BioRepository.get_by_id(
            bios[0]
        )

        if account and first_bio:

            success = await set_bio(
                account.session_string,
                first_bio.text
            )

            if success:

                rotation.current_index = (
                    1 % len(bios)
                )

                rotation.last_changed = (
                    datetime.utcnow()
                )

                await BioRotationRepository.save(
                    rotation
                )

    await state.clear()

    hours = interval // 3600

    if interval < 3600:
        interval_text = f"{interval // 60} Minutes"
    elif hours == 1:
        interval_text = "1 Hour"
    else:
        interval_text = f"{hours} Hours"

    await smart_edit(
        callback,
        f"""
✅ <b>Auto Bio Rotation Enabled</b>
━━━━━━━━━━━━━━━━━━━━━━━━━━
🟢 Status :<b>Enabled</b>

📝 Selected Bios :<b>{len(bios)}</b>

⏰ Interval :<b>{interval_text}</b>
━━━━━━━━━━━━━━━━━━━━━━━━━━
✅ First bio has been
applied immediately.

The remaining bios will
rotate automatically
after every :<b>{interval_text}</b>.
""",
        bio_home_keyboard()
    )