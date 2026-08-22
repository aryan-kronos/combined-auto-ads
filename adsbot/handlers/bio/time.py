# [Engineered & Developed by Aryan | https://t.me/thatonearyan]
from aiogram import Router, F
from aiogram.types import CallbackQuery
from aiogram.fsm.context import FSMContext

from utils.smart_edit import smart_edit
from keyboards.bio_time import time_keyboard

router = Router()


@router.callback_query(F.data == "bio_custom_time")
async def custom_time(
    callback: CallbackQuery,
    state: FSMContext
):

    await smart_edit(
        callback,
        """
🕒 <b>Custom Bio Rotation Time</b>
━━━━━━━━━━━━━━━━━━━━━━━━━━
•Choose how often your
Telegram bio should
change automatically.

⚠ Shorter intervals may
increase Telegram limits.

<b>Recommended:</b> 1 Hour
━━━━━━━━━━━━━━━━━━━━━━━━━━
""",
        time_keyboard()
    )




@router.callback_query(F.data.startswith("time_"))
async def save_interval(
    callback: CallbackQuery,
    state: FSMContext
):

    if callback.data == "time_custom":

        await callback.answer(
            """
Custom minutes
will be added
in the next update.
""",
            show_alert=True
        )
        return

    interval = int(
        callback.data.split("_")[1]
    )

    await state.update_data(
        interval=interval
    )

    names = {
        300: "5 Minutes",
        600: "10 Minutes",
        1800: "30 Minutes",
        3600: "1 Hour",
        7200: "2 Hours",
        21600: "6 Hours",
        43200: "12 Hours"
    }

    await smart_edit(
        callback,
        f"""
✅ <b>Interval Selected</b>
━━━━━━━━━━━━━━━━━━━━━━━━━━
Selected :<b>{names[interval]}</b>
━━━━━━━━━━━━━━━━━━━━━━━━━━
Click Continue to enable
Auto Bio Rotation.
""",
        __import__(
            "keyboards.bio_interval",
            fromlist=["interval_keyboard"]
        ).interval_keyboard()
    )