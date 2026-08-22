# [Engineered & Developed by Aryan | https://t.me/thatonearyan]
import asyncio
from datetime import datetime

from aiogram import Router, F
from aiogram.types import CallbackQuery
from aiogram.exceptions import TelegramBadRequest

from database.repository.campaign_repo import CampaignRepository

from keyboards.campaign import campaign_manage_keyboard
from utils.smart_edit import smart_edit
router = Router()

dashboard_tasks = {}


async def get_campaign(campaign_id: int):
    return await CampaignRepository.get_campaign(campaign_id)


def format_datetime(value):

    if not value:
        return "-"

    return value.strftime(
        "%d-%m-%Y %H:%M:%S"
    )


def format_runtime(started_at):

    if not started_at:
        return "-"

    runtime = datetime.utcnow() - started_at

    total = int(runtime.total_seconds())

    hours = total // 3600
    minutes = (total % 3600) // 60
    seconds = total % 60

    return (
        f"{hours:02}:{minutes:02}:{seconds:02}"
    )


async def live_dashboard(
    callback: CallbackQuery,
    campaign_id: int
):

    key = (
        callback.from_user.id,
        campaign_id
    )

    while True:

        campaign = await get_campaign(
            campaign_id
        )

        if not campaign:

            dashboard_tasks.pop(
                key,
                None
            )

            return


        if campaign.completed:

          if campaign.current_target == "Manually Finished":
             status = "🛑 Manually Finished"
          else:
             status = "✅ Finished"

        elif campaign.paused:

            status = "⏸ Paused"

        elif campaign.running:

           status = "🟢 Running"

        else:

           status = "🔴 Stopped"

        loop_text = (

            "♾ Infinite"

            if campaign.infinite

            else f"{campaign.completed_loops}/{campaign.loop_count}"

        )

        try:

            await callback.message.edit_text (

f""" 
🚀 <b>Campaign Dashboard</b>
━━━━━━━━━━━━━━━━━━━━━━━━━━
🆔 Campaign ID :<code>{campaign.id}</code>
🚦 Status :<b>{status}</b>
━━━━━━━━━━━━━━━━━━━━━━━━━━
📤 Messages Sent :<b>{campaign.total_sent}</b>
❌ Failed :<b>{campaign.failed_sent}</b>
🎯 Current Group :<b>{campaign.current_target or "Waiting..."}</b>
👥 Progress :<b>{loop_text}</b>
━━━━━━━━━━━━━━━━━━━━━━━━━━
⚡ Send Delay :<b>{campaign.send_delay} Seconds</b>
🔄 Repeat Delay :<b>{campaign.repeat_delay} Seconds</b>
━━━━━━━━━━━━━━━━━━━━━━━━━━
🕒 Started :<b>{format_datetime(campaign.started_at)}</b>
⌛ Runtime :<b>{format_runtime(campaign.started_at)}</b>
🏁 Finished :<b>{format_datetime(campaign.finished_at)}</b>

""",

reply_markup=campaign_manage_keyboard(
    campaign.id,
    running=campaign.running,
    completed=campaign.completed,
    paused=campaign.paused
)

            )

        except TelegramBadRequest:

            pass

        except Exception:

            dashboard_tasks.pop(
                key,
                None
            )

            return

        if (
            not campaign.running
            and
            not campaign.paused
        ):

            dashboard_tasks.pop(
                key,
                None
            )

            return

        await asyncio.sleep(2) 



@router.callback_query(
    F.data.startswith("campaign_manage_")
)
async def manage_campaign(
    callback: CallbackQuery
):

    campaign_id = int(
        callback.data.split("_")[2]
    )

    key = (
        callback.from_user.id,
        campaign_id
    )

    old_task = dashboard_tasks.get(
        key
    )

    if old_task:
        old_task.cancel()

    campaign = await get_campaign(
        campaign_id
    )

    if not campaign:

        await callback.answer(
            "Campaign not found.",
            show_alert=True
        )

        return

    dashboard_tasks[key] = asyncio.create_task(
        live_dashboard(
            callback,
            campaign_id
        )
    )

    await callback.answer()


@router.callback_query(
    F.data.startswith("start_campaign_")
)
async def start_campaign(
    callback: CallbackQuery
):

    campaign_id = int(
        callback.data.split("_")[2]
    )

    await CampaignRepository.update_status(campaign_id, True)

    await callback.answer(
        "▶ Campaign Started"
    )

    await manage_campaign(
        callback
    )



@router.callback_query(
    F.data.startswith("pause_campaign_")
)
async def pause_campaign(
    callback: CallbackQuery
):

    campaign_id = int(
        callback.data.split("_")[2]
    )

    await CampaignRepository.pause_campaign(campaign_id)

    await callback.answer(
        "⏸ Campaign Paused"
    )

    await manage_campaign(
        callback
    )


@router.callback_query(
    F.data.startswith("stop_campaign_")
)
async def stop_campaign(
    callback: CallbackQuery
):

    campaign_id = int(
        callback.data.split("_")[2]
    )

    campaign = await CampaignRepository.get_campaign(campaign_id)
    if campaign:
        campaign.running = False
        campaign.paused = False
        campaign.completed = True
        campaign.finished_at = datetime.utcnow()
        campaign.current_target = "Manually Finished"
        await CampaignRepository.save(campaign)

    task = dashboard_tasks.pop(
        (
            callback.from_user.id,
            campaign_id
        ),
        None
    )

    if task:
        task.cancel()

    await callback.answer(
        "🛑 Campaign Stopped Successfully",
        show_alert=True
    )

    campaign = await get_campaign(campaign_id)

    try:

        await smart_edit(
    callback,
            f"""
🚀 <b>Campaign Dashboard</b>
━━━━━━━━━━━━━━━━━━━━━━━━━━
🆔 Campaign ID : <code>{campaign.id}</code>
🚦 Status : <b>🛑 Manually Finished</b>
━━━━━━━━━━━━━━━━━━━━━━━━━━
📤 Messages Sent : <b>{campaign.total_sent}</b>
❌ Failed : <b>{campaign.failed_sent}</b>
🎯 Current Group : <b>Manually Finished</b>
👥 Progress : <b>{"♾ Infinite" if campaign.infinite else f"{campaign.completed_loops}/{campaign.loop_count}"}</b>
━━━━━━━━━━━━━━━━━━━━━━━━━━
⚡ Send Delay : <b>{campaign.send_delay} Seconds</b>
🔄 Repeat Delay : <b>{campaign.repeat_delay} Seconds</b>
━━━━━━━━━━━━━━━━━━━━━━━━━━
🕒 Started : <b>{format_datetime(campaign.started_at)}</b>
⌛ Runtime : <b>{format_runtime(campaign.started_at)}</b>
🏁 Finished : <b>{format_datetime(campaign.finished_at)}</b>
""",
            reply_markup=campaign_manage_keyboard(
                campaign.id,
                running=False,
                completed=True,
                paused=False
            )
        )

    except TelegramBadRequest:
        pass


@router.callback_query(
    F.data.startswith("resume_campaign_")
)
async def resume_campaign(
    callback: CallbackQuery
):

    campaign_id = int(
        callback.data.split("_")[2]
    )

    await CampaignRepository.resume_campaign(campaign_id)

    await callback.answer(
        "▶ Campaign Resumed"
    )

    await manage_campaign(
        callback
    )


@router.callback_query(
    F.data.startswith("delete_campaign_")
)
async def delete_campaign(
    callback: CallbackQuery
):

    campaign_id = int(
        callback.data.split("_")[2]
    )

    key = (
        callback.from_user.id,
        campaign_id
    )

    task = dashboard_tasks.pop(
        key,
        None
    )

    if task:
        task.cancel()

    await CampaignRepository.delete_campaign(campaign_id)

    # Return user to My Campaigns page immediately
    from handlers.campaign.my_campaigns import my_campaigns

    from handlers.campaign.my_campaigns import my_campaigns

    await callback.answer(
    "✅ Campaign Deleted Successfully"
)

    await my_campaigns(callback)
