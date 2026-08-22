# [Engineered & Developed by Aryan | https://t.me/thatonearyan]
from custom_emojis import button_emoji_id
from aiogram import Router, F
from aiogram.types import CallbackQuery
from aiogram.utils.keyboard import InlineKeyboardBuilder

from database.repository.campaign_repo import CampaignRepository
from utils.smart_edit import smart_edit
router = Router()


def loop_keyboard(campaign_id: int):

    kb = InlineKeyboardBuilder()

    loops = [1, 5, 10, 25, 50]

    for loop in loops:
        kb.button(
            text=f"🔁 {loop}x",
            callback_data=f"set_loop_{campaign_id}_{loop}"
        )

    kb.button(
        text="Infinite",
        callback_data=f"set_loop_{campaign_id}_inf",
        style="primary",
        icon_custom_emoji_id=button_emoji_id("5364087614930431949")
    )

    kb.button(
        text="Back",
        callback_data=f"open_campaign_{campaign_id}",
        style="danger",
        icon_custom_emoji_id=button_emoji_id("5409284148491726576")
    )

    kb.adjust(2, 2, 1, 1)

    return kb.as_markup()


@router.callback_query(
    F.data.startswith("loop_campaign_")
)
async def loop_menu(callback: CallbackQuery):

    campaign_id = int(
        callback.data.split("_")[2]
    )

    await smart_edit(
    callback,
        "🔁 <b>Select Loop Count</b>",
        reply_markup=loop_keyboard(
            campaign_id
        )
    )

    await callback.answer()


@router.callback_query(
    F.data.startswith("set_loop_")
)
async def set_loop(callback: CallbackQuery):

    data = callback.data.split("_")

    campaign_id = int(data[2])

    value = data[3]

    campaign = await CampaignRepository.get_campaign(campaign_id)
    if campaign:
        if value == "inf":
            campaign.infinite = True
            campaign.loop_count = 0
        else:
            campaign.infinite = False
            campaign.loop_count = int(value)
        campaign.completed_loops = 0
        await CampaignRepository.save(campaign)

    await callback.answer(
        "✅ Loop updated"
    )

    await smart_edit(
    callback,
        f"✅ Loop set to {'∞ Infinite' if value == 'inf' else value + 'x'}"
    )