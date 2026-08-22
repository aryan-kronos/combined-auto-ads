# [Engineered & Developed by Aryan | https://t.me/thatonearyan]
from aiogram import Router, F
from aiogram.types import CallbackQuery

from database.repository.account_repo import AccountRepository
from database.repository.campaign_repo import CampaignRepository
from database.repository.target_repo import TargetRepository

from keyboards.campaign import (
    campaign_list_keyboard,
    campaign_manage_keyboard,
)

from utils.smart_edit import smart_edit
from config import config

router = Router()


@router.callback_query(F.data == "my_campaigns")
async def my_campaigns(callback: CallbackQuery):

    user = await AccountRepository.get_user(
        callback.from_user.id
    )

    if not user:

        await callback.answer(
            "No account found.",
            show_alert=True
        )

        return

    campaigns = await CampaignRepository.get_user_campaigns(
        user.id
    )

    if not campaigns:

        await smart_edit(
            callback,
f"""
📂 <b>My Advertising Campaigns</b>
━━━━━━━━━━━━━━━━━━━━━━━━━━

<blockquote>
🤔 <b>No campaigns found!</b>
Create your first high-speed advertising campaign to start broadcasting messages to Telegram groups.
</blockquote>

<blockquote>
👉 Tap <b>Create Campaign</b> below to get started!
</blockquote>

{config.BRAND_FOOTER}
""",
            campaign_list_keyboard([])
        )

        return

    total = len(campaigns)

    running = len(
        [c for c in campaigns if c.running]
    )

    paused = len(
        [c for c in campaigns if c.paused]
    )

    finished = len(
        [c for c in campaigns if c.completed]
    )

    stopped = len(
        [
            c for c in campaigns
            if (
                not c.running
                and not c.paused
                and not c.completed
            )
        ]
    )

    await smart_edit(
        callback,
        f"""
📢 <b>My Advertising Campaigns</b>
━━━━━━━━━━━━━━━━━━━━━━━━━━

<blockquote>
📊 <b>Total Campaigns:</b> <code>{total}</code>
🟢 <b>Running:</b> <code>{running}</code> | ⏸ <b>Paused:</b> <code>{paused}</code>
✅ <b>Completed:</b> <code>{finished}</code> | 🔴 <b>Stopped:</b> <code>{stopped}</code>
</blockquote>

<blockquote>
👇 <b>Select a campaign below to view live telemetry or manage broadcast:</b>
</blockquote>

{config.BRAND_FOOTER}
""",
        campaign_list_keyboard(campaigns)
    )


@router.callback_query(
    F.data.startswith("open_campaign_")
)
async def open_campaign(callback: CallbackQuery):

    campaign_id = int(
        callback.data.split("_")[2]
    )

    campaign = await CampaignRepository.get_campaign(
        campaign_id
    )

    if not campaign:

        await callback.answer(
            "Campaign not found.",
            show_alert=True
        )

        return

    targets = await TargetRepository.get_targets(
        campaign.id
    )

    if campaign.completed:
        status = "✅ Finished"
    elif campaign.running:
        status = "🟢 Running"
    elif campaign.paused:
        status = "⏸ Paused"
    else:
        status = "🔴 Stopped"

    await smart_edit(
        callback,
        f"""
📢 <b>Campaign Details & Live Controls</b>
━━━━━━━━━━━━━━━━━━━━━━━━━━

<blockquote>
🆔 <b>Campaign ID:</b> <code>{campaign.id}</code>
🚦 <b>Status:</b> <b>{status}</b>
👥 <b>Target Groups:</b> <code>{len(targets)}</code>
📊 <b>Delivered Messages:</b> <code>{campaign.total_sent:,}</code>
⏱ <b>Group Delay:</b> <code>{campaign.send_delay}s</code> | 🔁 <b>Loop Delay:</b> <code>{campaign.repeat_delay}s</code>
📅 <b>Created:</b> <code>{campaign.created_at.strftime("%d-%m-%Y %H:%M")}</code>
</blockquote>

<blockquote>
📨 <b>Broadcast Preview:</b>
{campaign.post_data}
</blockquote>

{config.BRAND_FOOTER}
""",
        campaign_manage_keyboard(
            campaign.id,
            campaign.running,
            campaign.completed,
            campaign.paused
        )
    )