# [Engineered & Developed by Aryan | https://t.me/thatonearyan]
from aiogram import Router, F
from aiogram.types import CallbackQuery

from database.repository.campaign_repo import CampaignRepository
from utils.smart_edit import smart_edit
router = Router()


@router.callback_query(F.data.startswith("start_campaign_"))
async def start_campaign(callback: CallbackQuery):

    campaign_id = int(
        callback.data.split("_")[2]
    )

    await CampaignRepository.update_status(
        campaign_id,
        True
    )

    await callback.answer(
        "▶ Campaign Started"
    )


@router.callback_query(F.data.startswith("stop_campaign_"))
async def stop_campaign(callback: CallbackQuery):

    campaign_id = int(
        callback.data.split("_")[2]
    )

    await CampaignRepository.update_status(
        campaign_id,
        False
    )

    await callback.answer(
        "⏹ Campaign Stopped"
    )


@router.callback_query(F.data.startswith("pause_campaign_"))
async def pause_campaign(callback: CallbackQuery):

    campaign_id = int(
        callback.data.split("_")[2]
    )

    await CampaignRepository.pause_campaign(
        campaign_id
    )

    await callback.answer(
        "⏸ Campaign Paused"
    )


@router.callback_query(F.data.startswith("resume_campaign_"))
async def resume_campaign(callback: CallbackQuery):

    campaign_id = int(
        callback.data.split("_")[2]
    )

    await CampaignRepository.resume_campaign(
        campaign_id
    )

    await callback.answer(
        "▶ Campaign Resumed"
    )


@router.callback_query(F.data.startswith("loop_campaign_"))
async def loop_campaign(callback: CallbackQuery):

    await callback.answer()

    await smart_edit(
    callback,
        "🔁 Loop settings will be added in the next update."
    )


@router.callback_query(F.data.startswith("interval_campaign_"))
async def interval_campaign(callback: CallbackQuery):

    await callback.answer()

    await smart_edit(
    callback,
        "⏱ Interval settings will be added in the next update."
    )


@router.callback_query(F.data.startswith("schedule_campaign_"))
async def schedule_campaign(callback: CallbackQuery):

    await callback.answer()

    await smart_edit(
    callback,
        "📅 Scheduler will be added in the next update."
    )


@router.callback_query(F.data.startswith("stats_campaign_"))
async def stats_campaign(callback: CallbackQuery):

    await callback.answer()

    await smart_edit(
    callback,
        "📊 Statistics panel coming soon."
    )


@router.callback_query(F.data.startswith("delete_campaign_"))
async def delete_campaign(callback: CallbackQuery):

    campaign_id = int(
        callback.data.split("_")[2]
    )

    await CampaignRepository.delete_campaign(
        campaign_id
    )

    await smart_edit(
    callback,
        "🗑 Campaign Deleted Successfully."
    )

    await callback.answer()