# [Engineered & Developed by Aryan | https://t.me/thatonearyan]
from aiogram import Router, F
from aiogram.types import (
    CallbackQuery,
    Message
)
from aiogram.fsm.context import FSMContext

from database.repository.user_repo import UserRepository
from database.repository.bio_repo import BioRepository

from keyboards.bio import (
    back_keyboard,
    bio_home_keyboard
)

from states.bio import BioState
from utils.smart_edit import smart_edit

router = Router()


@router.callback_query(F.data == "bio_add")
async def add_bio(callback: CallbackQuery, state: FSMContext):

    user = await UserRepository.get_user(
        callback.from_user.id
    )

    bios = await BioRepository.get_bios(
        user.id
    )

    if len(bios) >= 5:

        await callback.answer(
            """
❌ BIO LIMIT REACHED
━━━━━━━━━━━━━━━━━━━━━━━━━━
You can store a maximum
of 5 bios.

Delete an existing bio
before adding a new one.
""",
            show_alert=True
        )
        return

    await state.set_state(
        BioState.waiting_bio
    )

    await smart_edit(
        callback,
        """
📝 <b>Add New Bio</b>
━━━━━━━━━━━━━━━━━━━━━━━━━━
Send the bio text.
• Maximum 70 characters.
• Type /cancel to cancel.
━━━━━━━━━━━━━━━━━━━━━━━━━━
""",
        back_keyboard()
    )

    await callback.answer()


@router.message(BioState.waiting_bio)
async def save_bio(message: Message, state: FSMContext):

    text = message.text.strip()

    if len(text) > 70:

        await message.answer(
            """
❌ Bio is too long.

Maximum allowed length
is 70 characters.
"""
        )
        return

    user = await UserRepository.get_user(
        message.from_user.id
    )

    bios = await BioRepository.get_bios(
        user.id
    )

    if len(bios) >= 5:

        await message.answer(
            """
❌ You already have
5 saved bios.
"""
        )

        await state.clear()
        return

    await BioRepository.add(
        user.id,
        text
    )

    total = await BioRepository.count(
        user.id
    )

    await state.clear()

    from keyboards.bio import back_keyboard

    await message.answer(
    f"""
✅ <b>Bio Added Successfully</b>
━━━━━━━━━━━━━━━━━━━━━━━━━━
•Your bio has been saved.
📝 Total Bios :<b>{total} / 5</b>
""",
    reply_markup=back_keyboard()
)