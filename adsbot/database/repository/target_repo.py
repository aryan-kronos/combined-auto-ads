# [Engineered & Developed by Aryan | https://t.me/thatonearyan]
from datetime import datetime
from database.session import db, get_next_id
from database.models.campaign_target import CampaignTarget

COL = db.campaign_targets

def _obj(d): return CampaignTarget(**{k: d.get(k) for k in ("id","campaign_id","chat_id","chat_username","chat_title","created_at")})

class TargetRepository:
    @staticmethod
    async def get_targets(campaign_id: int):
        return [_obj(d) async for d in COL.find({"campaign_id": campaign_id})]

    @staticmethod
    async def add_target(campaign_id: int, chat_id: int, chat_username=None, chat_title=None):
        d = {"id": await get_next_id("campaign_targets"), "campaign_id": campaign_id, "chat_id": chat_id,
             "chat_username": chat_username, "chat_title": chat_title, "created_at": datetime.utcnow()}
        await COL.insert_one(d)
        return _obj(d)

    @staticmethod
    async def delete_campaign_targets(campaign_id: int):
        await COL.delete_many({"campaign_id": campaign_id})
