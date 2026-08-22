# [Engineered & Developed by Aryan | https://t.me/thatonearyan]
from aiogram import Router, F
from aiogram.types import CallbackQuery
from aiogram.fsm.context import FSMContext

from database.repository.user_repo import UserRepository
from database.repository.bio_repo import BioRepository

from keyboards.bio import continue_keyboard
from utils.smart_edit import smart_edit
from keyboards.bio_interval import interval_keyboard


router = Router()


@router.callback_query(
    F.data.startswith("bio_select_")
)
async def select_bio(
    callback: CallbackQuery,
    state: FSMContext
):
    await callback.answer(cache_time=1)

    bio_id = int(callback.data.split("_")[2])

    data = await state.get_data()

    selected = list(
        data.get("selected_bios", [])
    )

    if bio_id in selected:
        selected.remove(bio_id)
    else:
        if len(selected) >= 5:
            await callback.answer(
                "Maximum 5 bios allowed.",
                show_alert=True
            )
            return

        selected.append(bio_id)

    await state.update_data(
        selected_bios=selected
    )

    user = await UserRepository.get_user(
        callback.from_user.id
    )

    bios = await BioRepository.get_bios(
        user.id
    )

    text = f"""
📝 <b>Select Bios</b>
━━━━━━━━━━━━━━━━━━━━━━━━━━
• Selected : <b>{len(selected)} / 5</b>

• Minimum Required : <b>2</b>
━━━━━━━━━━━━━━━━━━━━━━━━━━
"""

    buttons = []

    for bio in bios:

        preview = bio.text

        if len(preview) > 35:
            preview = preview[:35] + "..."

        buttons.append(
            (
                f'{"✅" if bio.id in selected else "☑"} {preview}',
                f"bio_select_{bio.id}"
            )
        )

    try:
        await smart_edit(
            callback,
            text,
            continue_keyboard(
                buttons,
                len(selected)
            )
        )
    except Exception:
        pass


@router.callback_query(
    F.data == "bio_continue"
)
async def continue_rotation(
    callback: CallbackQuery,
    state: FSMContext
):

    data = await state.get_data()

    selected = data.get(
        "selected_bios",
        []
    )

    if len(selected) < 2:

        await callback.answer(
            """
Please select at least
2 bios.
""",
            show_alert=True
        )
        return

    await smart_edit(
        callback,
        """
⏰ <b>Rotation Interval</b>
━━━━━━━━━━━━━━━━━━━━━━━━━━

•Default Interval :<b>1 Hour</b>
•Recommended for account safety.
━━━━━━━━━━━━━━━━━━━━━━━━━━
""",
        interval_keyboard()
    )

    await callback.answer()