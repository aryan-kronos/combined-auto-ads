# [Engineered & Developed by Aryan | https://t.me/thatonearyan]
from custom_emojis import button_emoji_id
from aiogram import Router, F
from aiogram.types import CallbackQuery
from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.fsm.context import FSMContext

from database.repository.user_repo import UserRepository
from database.repository.bio_repo import BioRepository
from database.repository.bio_rotation_repo import BioRotationRepository

from states.bio import BioState
from utils.smart_edit import smart_edit

router = Router()


@router.callback_query(
    F.data.startswith("bio_account_")
)
async def select_account(
    callback: CallbackQuery,
    state: FSMContext
):

    account_id = int(
        callback.data.split("_")[2]
    )

    rotation = await BioRotationRepository.get(
        account_id
    )

    if rotation and rotation.enabled:

        await callback.answer(
            """
⚠ ALREADY ENABLED

This account is already
using Auto Bio Rotation.

Disable it first if you
want to configure it again.
""",
            show_alert=True
        )

        return

    await state.update_data(
        account_id=account_id
    )

    await state.set_state(
        BioState.selecting_bios
    )

    user = await UserRepository.get_user(
        callback.from_user.id
    )

    bios = await BioRepository.get_bios(
        user.id
    )

    kb = InlineKeyboardBuilder()

    for bio in bios:

        preview = bio.text

        if len(preview) > 35:
            preview = preview[:35] + "..."

        kb.button(
            text=f"☑ {preview}",
            callback_data=f"bio_select_{bio.id}",
            style="primary",
        )

    kb.button(
        text="Continue (0)",
        callback_data="bio_finish_selection",
        style="success",
        icon_custom_emoji_id=button_emoji_id("4987757216040747796")
    )

    kb.button(
        text="Back",
        callback_data="bio_enable",
        style="danger",
        icon_custom_emoji_id=button_emoji_id("5409284148491726576")
    )

    kb.adjust(1)

    await smart_edit(
        callback,
        """
📝 <b>Select Bios</b>
━━━━━━━━━━━━━━━━━━━━━━━━━━
•Select at least :<b>2 Bios</b>.
•Maximum allowed :<b>5 Bios</b>.
━━━━━━━━━━━━━━━━━━━━━━━━━━
""",
        kb.as_markup()
    )