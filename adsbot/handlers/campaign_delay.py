# [Engineered & Developed by Aryan | https://t.me/thatonearyan]
from aiogram import Router, F
from aiogram.types import CallbackQuery
from aiogram.fsm.context import FSMContext

from handlers.campaign.create_campaign import CampaignState
from keyboards.confirm import confirm_campaign_keyboard
from utils.smart_edit import smart_edit
router = Router()


@router.callback_query(
    F.data.startswith("delay_")
)
async def select_delay(
    callback: CallbackQuery,
    state: FSMContext
):

    delay = int(
        callback.data.split("_")[1]
    )

    await state.update_data(
        send_delay=delay
    )

    await state.set_state(
        CampaignState.waiting_confirm
    )

    data = await state.get_data()

    if data.get("infinite"):
        loop_text = "∞ Infinite"
    else:
        loop_text = str(data["loop_count"])

    # Delay Text
    if delay == 60:

        delay_text = "60 Seconds"

    elif delay < 3600:

        delay_text = f"{delay // 60} Minute(s)"

    elif delay == 86400:

        delay_text = "24 Hours"

    elif delay < 86400:

        delay_text = f"{delay // 3600} Hour(s)"

    else:

        delay_text = f"{delay} Seconds"

    await smart_edit(
    callback,
        f"""
📋 <b>Campaign Summary</b>
━━━━━━━━━━━━━━━━━━━━━━━━━━
🔁 Loops: <b>{loop_text}</b>

⏱ Loop Delay: <b>{delay_text}</b>
━━━━━━━━━━━━━━━━━━━━━━━━━━
⚠️ <i>Lower delay increases the risk of spam detection and account limitations.</i>
🚀 Ready to start?
""",
        reply_markup=confirm_campaign_keyboard()
    )

    await callback.answer()


@router.callback_query(
    F.data == "premium_delay"
)
async def premium_delay(
    callback: CallbackQuery
):

    await callback.answer(
        "⭐ This feature is available for Premium users only.",
        show_alert=True
    )


@router.callback_query(
    F.data == "delay_custom"
)
async def custom_delay(
    callback: CallbackQuery
):

    await callback.answer(
        "🚧 Custom delay will be available soon.",
        show_alert=True
    )


@router.callback_query(
    F.data == "ignore"
)
async def ignore(
    callback: CallbackQuery
):

    await callback.answer()