# [Engineered & Developed by Aryan | https://t.me/thatonearyan]
from aiogram import Router, F
from aiogram.types import CallbackQuery

import asyncio

from database.repository.campaign_repo import CampaignRepository
from database.repository.target_repo import TargetRepository

from services.campaign.campaign_worker import run_single_campaign
from utils.smart_edit import smart_edit
router = Router()


@router.callback_query(
    F.data == "start_campaign"
)
async def start_campaign(
    callback: CallbackQuery,
    state
):

    data = await state.get_data()

    campaign = await CampaignRepository.create(
        account_id=data["account_id"],
        post_data=data["post_data"],
    )

    # Fixed delay between groups
    await CampaignRepository.update_send_delay(
        campaign.id,
        3
    )

    # User selected loop delay
    await CampaignRepository.update_repeat_delay(
        campaign.id,
        data["send_delay"]
    )

    # Loop settings
    await CampaignRepository.update_loop(
        campaign.id,
        data["loop_count"],
        data["infinite"]
    )

    # ==========================
    # TARGETS
    # ==========================

    if data["target_type"] == "manual":

        groups = data["manual_groups"]

        selected = [
            g["id"]
            for g in groups
        ]

    else:

        groups = data["groups"]

        selected = data["selected_groups"]

    for group_id in selected:

        group = next(
            (
                g
                for g in groups
                if g["id"] == group_id
            ),
            None
        )

        await TargetRepository.add_target(
            campaign_id=campaign.id,
            chat_id=group_id,
            chat_username=(
                group.get("username")
                if group else None
            ),
            chat_title=(
                group.get("title")
                if group else None
            )
        )

    # ==========================
    # START CAMPAIGN
    # ==========================

    await CampaignRepository.update_status(
        campaign.id,
        True
    )

    asyncio.create_task(
        run_single_campaign(
            campaign.id
        )
    )

    delay = data["send_delay"]

    if delay == 60:

        delay_text = "60 Seconds"

    elif delay < 3600:

        delay_text = f"{delay // 60} Minute(s)"

    elif delay == 86400:

        delay_text = "24 Hours"

    else:

        delay_text = f"{delay // 3600} Hour(s)"

    await smart_edit(
    callback,
    f"""
✅ <b>Campaign Started Successfully</b>
━━━━━━━━━━━━━━━━━━━━━━━━━━
🆔 <b>Campaign ID</b> :<code>{campaign.id}</code>

👥 <b>Total Groups</b> :{len(selected)}

🔁 <b>Loops</b> :{"∞ Infinite" if data["infinite"] else data["loop_count"]}

⚡ <b>Between Groups</b> :3 Seconds

⏱ <b>Loop Delay</b> :{delay_text}

📡 <b>Status</b> :🟢 Running
━━━━━━━━━━━━━━━━━━━━━━━━━━
⚠️ Keep this account online until the campaign finishes.
"""
)

    await state.clear()

    await callback.answer(
        "Campaign Started!"
    )


@router.callback_query(
    F.data == "cancel_campaign"
)
async def cancel_campaign(
    callback: CallbackQuery,
    state
):

    await state.clear()

    await smart_edit(
    callback,
        "❌ Campaign Cancelled."
    )

    await callback.answer()