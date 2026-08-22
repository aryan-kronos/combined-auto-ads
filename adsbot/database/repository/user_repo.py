# [Engineered & Developed by Aryan | https://t.me/thatonearyan]
from datetime import datetime
from database.session import db, get_next_id
from database.models.user import User

COL = db.users

def _obj(d):
    return User(**{k: d.get(k) for k in (
        "id","telegram_id","username","first_name","account_slots","wallet",
        "is_premium","custom_bio","is_banned","created_at"
    )})

class UserRepository:
    @staticmethod
    async def get_user(telegram_id: int):
        d = await COL.find_one({"telegram_id": telegram_id})
        return _obj(d) if d else None

    @staticmethod
    async def create_user(telegram_id: int, username: str | None, first_name: str):
        existing = await COL.find_one({"telegram_id": telegram_id})
        if existing:
            return _obj(existing)
        user = {
            "id": await get_next_id("users"),
            "telegram_id": telegram_id,
            "username": username,
            "first_name": first_name,
            "account_slots": 1,
            "wallet": 0,
            "is_premium": False,
            "custom_bio": None,
            "is_banned": False,
            "created_at": datetime.utcnow(),
        }
        await COL.insert_one(user)
        return _obj(user)

    @staticmethod
    async def set_premium(telegram_id: int, premium: bool = True):
        r = await COL.update_one({"telegram_id": telegram_id}, {"$set": {"is_premium": premium}})
        return r.modified_count > 0 or r.matched_count > 0

    @staticmethod
    async def update_custom_bio(telegram_id: int, bio: str):
        await COL.update_one({"telegram_id": telegram_id}, {"$set": {"custom_bio": bio}})

    @staticmethod
    async def add_wallet(telegram_id: int, amount: int):
        await COL.update_one({"telegram_id": telegram_id}, {"$inc": {"wallet": amount}})

    @staticmethod
    async def remove_wallet(telegram_id: int, amount: int):
        await COL.update_one({"telegram_id": telegram_id}, {"$inc": {"wallet": -amount}})

    @staticmethod
    async def get_all_premium():
        return [_obj(d) async for d in COL.find({"is_premium": True})]

    @staticmethod
    async def get_all():
        return [_obj(d) async for d in COL.find({})]
