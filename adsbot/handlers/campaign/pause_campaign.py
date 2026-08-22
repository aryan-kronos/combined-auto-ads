# [Engineered & Developed by Aryan | https://t.me/thatonearyan]
from aiogram import Router, F
from aiogram.types import CallbackQuery

from database.repository.campaign_repo import CampaignRepository

router = Router()


@router.callback_query(
    F.data.startswith("pause_campaign_")
)
async def pause_campaign(
    callback: CallbackQuery
):

    campaign_id = int(
        callback.data.split("_")[2]
    )

    campaign = await CampaignRepository.get_campaign(
        campaign_id
    )

    if not campaign:

        await callback.answer(
            "Campaign not found",
            show_alert=True
        )

        return

    new_state = not campaign.paused

    await CampaignRepository.update_pause(
        campaign_id,
        new_state
    )

    # Resume campaign if unpaused
    if not new_state:

        await CampaignRepository.update_status(
            campaign_id,
            True
        )

    if new_state:

        text = "⏸ Campaign Paused"

    else:

        text = "▶ Campaign Resumed"

    await callback.answer(
        text
    )

    from handlers.campaign.manage_campaign import manage_campaign

    await manage_campaign(
        callback
    )