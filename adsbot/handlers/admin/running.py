# [Engineered & Developed by Aryan | https://t.me/thatonearyan]
from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message
from config import config
from database.repository.campaign_repo import CampaignRepository
from database.repository.account_repo import AccountRepository

router = Router()

@router.message(Command("running"))
async def running_campaigns(message: Message):
    if message.from_user.id not in config.ADMINS:
        return

    from database.session import db
    campaigns = []
    async for d in db.campaigns.find({"running": True}):
        c = await CampaignRepository.get_campaign(d["id"])
        if c:
            campaigns.append(c)

    if not campaigns:
        await message.answer("✅ No campaigns are currently running.")
        return

    text = "🚀 <b>LIVE RUNNING CAMPAIGNS</b>\n\nTotal Running: <b>%s</b>\n\n" % len(campaigns)
    for campaign in campaigns:
        account = await AccountRepository.get_account(campaign.account_id)
        user = await AccountRepository.get_user_by_id(account.user_id) if account else None
        text += (
            "━━━━━━━━━━━━━━\n\n"
            f"🆔 <b>Campaign #{campaign.id}</b>\n\n"
            f"👤 User : <b>{user.first_name if user else 'Unknown'}</b>\n"
            f"📱 Account : <b>{account.account_name if account else 'Unknown'}</b>\n"
            f"🎯 Current : <b>{campaign.current_target or 'Starting...'}</b>\n"
            f"📤 Sent : <b>{campaign.total_sent}</b>\n"
            f"❌ Failed : <b>{campaign.failed_sent}</b>\n"
            f"🔁 Loop : <b>{'∞' if campaign.infinite else f'{campaign.completed_loops}/{campaign.loop_count}'}</b>\n\n"
        )
    await message.answer(text)
