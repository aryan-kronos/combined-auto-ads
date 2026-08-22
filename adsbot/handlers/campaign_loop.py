# [Engineered & Developed by Aryan | https://t.me/thatonearyan]
from aiogram import Router, F
from aiogram.types import CallbackQuery
from aiogram.fsm.context import FSMContext

from handlers.campaign.create_campaign import CampaignState
from keyboards.delay import delay_keyboard
from utils.smart_edit import smart_edit
router = Router()


@router.callback_query(
    F.data.startswith("loop_")
)
async def select_loop(
    callback: CallbackQuery,
    state: FSMContext
):

    value = callback.data.split("_")[1]

    if value == "infinite":

        await state.update_data(
            infinite=True,
            loop_count=999999999
        )

    else:

        await state.update_data(
            infinite=False,
            loop_count=int(value)
        )

    await state.set_state(
    CampaignState.waiting_delay
)

    await smart_edit(
    callback,
        "⏱ <b>Select Campaign Delay</b>",
        reply_markup=delay_keyboard(False)
    )

    await callback.answer()


@router.callback_query(
    F.data == "premium_loop"
)
async def premium_loop(
    callback: CallbackQuery
):

    await callback.answer(
        "⭐ Premium Feature",
        show_alert=True
    )