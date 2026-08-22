# [Engineered & Developed by Aryan | https://t.me/thatonearyan]
import asyncio
from datetime import datetime
from pyrogram import Client
from pyrogram.errors import FloodWait, RPCError

from config import config
from loader import bot
from database.repository.campaign_repo import CampaignRepository
from database.repository.account_repo import AccountRepository

running_campaigns = set()

async def process_campaign(campaign):
    campaign_id = campaign.id
    if campaign_id in running_campaigns:
        print(f"⚠️ Campaign #{campaign_id} already running")
        return

    running_campaigns.add(campaign_id)
    app = None
    sent_count = failed_count = 0

    try:
        campaign.started_at = datetime.utcnow()
        await CampaignRepository.save(campaign)

        account = await AccountRepository.get_account(campaign.account_id)
        if not account:
            campaign.running = False
            campaign.paused = False
            campaign.completed = True
            campaign.finished_at = datetime.utcnow()
            await CampaignRepository.save(campaign)
            return

        user = await AccountRepository.get_user_by_id(account.user_id)
        if not user:
            return

        owner_id = user.telegram_id
        targets = await CampaignRepository.get_targets(campaign_id)
        if not targets:
            campaign.running = False
            campaign.paused = False
            campaign.completed = True
            campaign.finished_at = datetime.utcnow()
            await CampaignRepository.save(campaign)
            await bot.send_message(owner_id, "❌ Campaign cancelled because no target groups were found.")
            return

        app = Client(
            f"campaign_{campaign_id}",
            api_id=config.API_ID,
            api_hash=config.API_HASH,
            session_string=account.session_string,
            in_memory=True,
        )
        await app.start()
        async for _ in app.get_dialogs():
            pass
        print("✅ Telegram Ready")

        loop_limit = 999999999 if campaign.infinite else max(campaign.loop_count, 1)

        while campaign.running and campaign.completed_loops < loop_limit:
            campaign = await CampaignRepository.get_campaign(campaign_id)
            if not campaign:
                break

            if campaign.paused:
                await asyncio.sleep(2)
                continue

            for target in targets:
                campaign = await CampaignRepository.get_campaign(campaign_id)
                if not campaign or not campaign.running or campaign.paused:
                    break

                try:
                    await app.send_message(target.chat_id, campaign.post_data or "")
                    sent_count += 1
                    campaign.total_sent += 1
                    campaign.current_target = target.chat_title or str(target.chat_id)
                    await CampaignRepository.save(campaign)
                    print(f"📤 Sent : {target.chat_title or target.chat_id}")
                    await asyncio.sleep(campaign.send_delay)

                except FloodWait as e:
                    print(f"⏳ FloodWait {e.value}s")
                    await asyncio.sleep(e.value)

                except (RPCError, Exception) as e:
                    failed_count += 1
                    campaign.failed_sent += 1
                    await CampaignRepository.save(campaign)
                    print(f"❌ Send Error: {e}")

            campaign = await CampaignRepository.get_campaign(campaign_id)
            if not campaign:
                break

            campaign.completed_loops += 1
            await CampaignRepository.save(campaign)

            if not campaign.infinite and campaign.completed_loops >= loop_limit:
                break

            if not campaign.running or campaign.paused:
                continue

            await asyncio.sleep(campaign.repeat_delay)

        campaign = await CampaignRepository.get_campaign(campaign_id)
        if campaign and campaign.current_target != "Manually Finished":
            campaign.finished_at = datetime.utcnow()
            campaign.current_target = "Completed"
            campaign.running = False
            campaign.paused = False
            campaign.completed = True
            await CampaignRepository.save(campaign)

            runtime = campaign.finished_at - campaign.started_at if campaign.started_at else None
            await bot.send_message(
                owner_id,
                f"""🎉 <b>Campaign Completed</b>
--------------------------------------------------
🆔 <code>{campaign.id}</code>
📤 Sent : {campaign.total_sent}
❌ Failed : {campaign.failed_sent}
👥 Groups : {len(targets)}
🔁 Loops : {"∞" if campaign.infinite else campaign.completed_loops}
⏱ Runtime : {str(runtime).split(".")[0] if runtime else "-"}
--------------------------------------------------
✅ Campaign Finished Successfully."""
            )

    except Exception as e:
        print(f"❌ Campaign Error: {e}")
        try:
            campaign = await CampaignRepository.get_campaign(campaign_id)
            if campaign:
                campaign.finished_at = datetime.utcnow()
                campaign.current_target = "Error"
                campaign.running = False
                campaign.paused = False
                campaign.completed = True
                await CampaignRepository.save(campaign)
        except Exception as save_error:
            print(f"❌ Failed to save campaign error state: {save_error}")
    finally:
        running_campaigns.discard(campaign_id)
        if app:
            try:
                await app.stop()
            except Exception:
                pass

async def run_single_campaign(campaign_id: int):
    campaign = await CampaignRepository.get_campaign(campaign_id)
    if not campaign:
        print(f"❌ Campaign {campaign_id} not found")
        return
    await process_campaign(campaign)

async def run_campaigns():
    print("🚀 Campaign Worker Started")
    while True:
        try:
            from database.session import db
            campaigns = []
            async for d in db.campaigns.find({"running": True}):
                campaign = await CampaignRepository.get_campaign(d["id"])
                if campaign:
                    campaigns.append(campaign)
            for campaign in campaigns:
                if campaign.id not in running_campaigns:
                    asyncio.create_task(run_single_campaign(campaign.id))
        except Exception as e:
            print("❌ Worker Error:", e)
        await asyncio.sleep(3)
