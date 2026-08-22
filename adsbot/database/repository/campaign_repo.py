# [Engineered & Developed by Aryan | https://t.me/thatonearyan]
from datetime import datetime
from database.session import db, get_next_id
from database.models.campaign import Campaign
from database.models.campaign_target import CampaignTarget

CAMPAIGNS = db.campaigns
TARGETS = db.campaign_targets
ACCOUNTS = db.accounts

def _campaign(d):
    fields = ("id","account_id","title","post_data","send_delay","repeat_delay","total_sent","failed_sent",
              "current_target","started_at","finished_at","running","completed","loop_count","completed_loops",
              "infinite","paused","scheduled_at","last_run","next_run","created_at")
    return Campaign(**{k: d.get(k) for k in fields})

def _target(d):
    return CampaignTarget(**{k: d.get(k) for k in ("id","campaign_id","chat_id","chat_username","chat_title","created_at")})

async def _update(cid, values):
    r = await CAMPAIGNS.update_one({"id": cid}, {"$set": values})
    if not r.matched_count:
        return None
    return await CampaignRepository.get_campaign(cid)

class CampaignRepository:
    @staticmethod
    async def create(account_id: int, post_data: str):
        d = {
            "id": await get_next_id("campaigns"), "account_id": account_id, "title": "New Campaign",
            "post_data": post_data, "send_delay": 5, "repeat_delay": 86400,
            "total_sent": 0, "failed_sent": 0, "current_target": None,
            "started_at": None, "finished_at": None, "running": False, "completed": False,
            "loop_count": 1, "completed_loops": 0, "infinite": False, "paused": False,
            "scheduled_at": None, "last_run": None, "next_run": None, "created_at": datetime.utcnow()
        }
        await CAMPAIGNS.insert_one(d)
        return _campaign(d)

    @staticmethod
    async def add_target(campaign_id: int, chat_id, chat_username=None, chat_title=None):
        d = {"id": await get_next_id("campaign_targets"), "campaign_id": campaign_id, "chat_id": chat_id,
             "chat_username": chat_username, "chat_title": chat_title, "created_at": datetime.utcnow()}
        await TARGETS.insert_one(d)
        return _target(d)

    @staticmethod
    async def get_targets(campaign_id: int):
        return [_target(d) async for d in TARGETS.find({"campaign_id": campaign_id})]

    @staticmethod
    async def get_user_campaigns(user_id: int):
        account_ids = [d["id"] async for d in ACCOUNTS.find({"user_id": user_id}, {"id": 1})]
        if not account_ids:
            return []
        return [_campaign(d) async for d in CAMPAIGNS.find({"account_id": {"$in": account_ids}})]

    @staticmethod
    async def get_campaign(campaign_id: int):
        d = await CAMPAIGNS.find_one({"id": campaign_id})
        return _campaign(d) if d else None

    @staticmethod
    async def delete_campaign(campaign_id: int):
        await CAMPAIGNS.delete_one({"id": campaign_id})
        await TARGETS.delete_many({"campaign_id": campaign_id})

    @staticmethod
    async def update_status(campaign_id: int, running: bool):
        values = {"running": running}
        if running:
            values.update(paused=False, completed=False, finished_at=None)
        else:
            values.update(paused=False, current_target="Stopped")
        return await _update(campaign_id, values)

    @staticmethod
    async def pause_campaign(campaign_id: int):
        return await _update(campaign_id, {"paused": True})

    @staticmethod
    async def resume_campaign(campaign_id: int):
        return await _update(campaign_id, {"paused": False, "running": True})

    @staticmethod
    async def update_send_delay(campaign_id: int, delay: int):
        return await _update(campaign_id, {"send_delay": delay})

    @staticmethod
    async def update_repeat_delay(campaign_id: int, delay: int):
        return await _update(campaign_id, {"repeat_delay": delay})

    @staticmethod
    async def update_loop(campaign_id: int, loops: int, infinite: bool = False):
        return await _update(campaign_id, {"loop_count": loops, "infinite": infinite})

    @staticmethod
    async def save(campaign):
        return await _update(campaign.id, {
            "account_id": campaign.account_id, "title": campaign.title, "post_data": campaign.post_data,
            "send_delay": campaign.send_delay, "repeat_delay": campaign.repeat_delay,
            "total_sent": campaign.total_sent, "failed_sent": campaign.failed_sent,
            "current_target": campaign.current_target, "started_at": campaign.started_at,
            "finished_at": campaign.finished_at, "running": campaign.running,
            "completed": campaign.completed, "loop_count": campaign.loop_count,
            "completed_loops": campaign.completed_loops, "infinite": campaign.infinite,
            "paused": campaign.paused, "scheduled_at": campaign.scheduled_at,
            "last_run": campaign.last_run, "next_run": campaign.next_run
        })

    @staticmethod
    async def update_pause(campaign_id: int, paused: bool):
        return await _update(campaign_id, {"paused": paused})

    @staticmethod
    async def count_user_campaigns(user_id: int):
        account_ids = [d["id"] async for d in ACCOUNTS.find({"user_id": user_id}, {"id": 1})]
        return await CAMPAIGNS.count_documents({"account_id": {"$in": account_ids}}) if account_ids else 0
