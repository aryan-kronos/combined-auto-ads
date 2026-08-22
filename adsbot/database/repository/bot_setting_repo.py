# [Engineered & Developed by Aryan | https://t.me/thatonearyan]
from datetime import datetime
from database.session import db, get_next_id
from database.models.bot_setting import BotSetting

COL = db.bot_settings

def _obj(d): return BotSetting(**{k: d.get(k) for k in ("id","page","text","media_type","file_id","updated_by","updated_at")})

class BotSettingRepository:
    @staticmethod
    async def get(page: str):
        d = await COL.find_one({"page": page})
        return _obj(d) if d else None

    @staticmethod
    async def save(page: str, text: str | None, media_type: str | None, file_id: str | None, admin_id: int):
        now = datetime.utcnow()
        d = await COL.find_one_and_update(
            {"page": page},
            {"$set": {"text": text, "media_type": media_type, "file_id": file_id, "updated_by": admin_id, "updated_at": now},
             "$setOnInsert": {"id": await get_next_id("bot_settings")}},
            upsert=True,
            return_document=True,
        )
        return _obj(d)
