# [Engineered & Developed by Aryan | https://t.me/thatonearyan]
from custom_emojis import button_emoji_id
from aiogram import Router, F
from aiogram.types import CallbackQuery
from aiogram.utils.keyboard import InlineKeyboardBuilder

from database.repository.user_repo import UserRepository
from database.repository.bio_repo import BioRepository
from database.repository.bio_rotation_repo import (
    BioRotationRepository
)
from database.repository.bio_rotation_item_repo import (
    BioRotationItemRepository
)

from handlers.bio.menu import bio_home
from utils.smart_edit import smart_edit

router = Router()


@router.callback_query(F.data == "bio_delete")
async def delete_bio_menu(callback: CallbackQuery):

    user = await UserRepository.get_user(
        callback.from_user.id
    )

    bios = await BioRepository.get_bios(
        user.id
    )

    if not bios:

        await callback.answer(
            """
❌ No Bios Found

Please add a bio first.
""",
            show_alert=True
        )
        return

    kb = InlineKeyboardBuilder()

    for bio in bios:

        preview = bio.text[:30]

        if len(bio.text) > 30:
            preview += "..."

        kb.button(
            text=preview,
            callback_data=f"delete_bio_{bio.id}",
            style="primary"
        )

    kb.button(
        text="Back",
        callback_data="bio_home",
        style="danger",
        icon_custom_emoji_id=button_emoji_id("5193119436621494267")
    )

    kb.adjust(1)

    await smart_edit(
    callback,
        """
🗑 <b>Select Bio To Delete</b>
━━━━━━━━━━━━━━━━━━━━━━━━━━
•Select the bio you want
to permanently remove.

•This action cannot
be undone.
━━━━━━━━━━━━━━━━━━━━━━━━━━
""",
        reply_markup=kb.as_markup()
    )

    await callback.answer()


@router.callback_query(
    F.data.startswith("delete_bio_")
)
async def delete_bio(callback: CallbackQuery):

    bio_id = int(
        callback.data.split("_")[2]
    )

    # Delete bio
    await BioRepository.delete(
        bio_id
    )

    # Remove this bio from every rotation
    await BioRotationItemRepository.delete_bio(
        bio_id
    )

    # Check every running rotation
    rotations = await BioRotationRepository.get_running()

    for rotation in rotations:

        items = await BioRotationItemRepository.get_bios(
            rotation.id
        )

        # Disable rotation if less than 2 bios remain
        if len(items) < 2:

            await BioRotationRepository.disable(
                rotation.account_id
            )

    await callback.answer(
        """
✅ Bio Deleted Successfully
""",
        show_alert=True
    )

    await bio_home(callback)