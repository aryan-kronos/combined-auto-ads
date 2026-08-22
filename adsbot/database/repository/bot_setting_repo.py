# [Engineered & Developed by Aryan | https://t.me/thatonearyan]
from datetime import datetime
from database.session import db, get_next_id
from database.models.bot_setting import BotSetting
from config import config

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

    @staticmethod
    async def get_upi() -> tuple[str, str]:
        d = await COL.find_one({"page": "upi_config"})
        if d and d.get("text"):
            parts = d["text"].split("|", 1)
            upi_id = parts[0].strip()
            upi_name = parts[1].strip() if len(parts) > 1 else config.UPI_NAME
            return upi_id, upi_name
        return config.UPI_ID, config.UPI_NAME

    @staticmethod
    async def set_upi(upi_id: str, upi_name: str, admin_id: int):
        now = datetime.utcnow()
        await COL.find_one_and_update(
            {"page": "upi_config"},
            {"$set": {"text": f"{upi_id}|{upi_name}", "updated_by": admin_id, "updated_at": now}},
            upsert=True
        )
