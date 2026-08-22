# [Engineered & Developed by Aryan | https://t.me/thatonearyan]
from datetime import datetime
from database.session import db, get_next_id
from database.models.bio_rotation import BioRotation

COL = db.bio_rotations

def _obj(d): return BioRotation(**{k: d.get(k) for k in ("id","account_id","enabled","interval","current_index","last_changed")})

class BioRotationRepository:
    @staticmethod
    async def create(account_id: int, interval: int = 3600):
        d = await COL.find_one({"account_id": account_id}, sort=[("id", -1)])
        if d:
            await COL.update_one({"_id": d["_id"]}, {"$set": {"enabled": True, "interval": interval}})
            d.update(enabled=True, interval=interval)
            return _obj(d)
        d = {"id": await get_next_id("bio_rotations"), "account_id": account_id, "enabled": True,
             "interval": interval, "current_index": 0, "last_changed": datetime.utcnow()}
        await COL.insert_one(d)
        return _obj(d)

    @staticmethod
    async def get(account_id: int):
        d = await COL.find_one({"account_id": account_id}, sort=[("id", -1)])
        return _obj(d) if d else None

    @staticmethod
    async def get_running():
        return [_obj(d) async for d in COL.find({"enabled": True})]

    @staticmethod
    async def disable(account_id: int):
        d = await COL.find_one({"account_id": account_id}, sort=[("id", -1)])
        if not d: return False
        await COL.update_one({"_id": d["_id"]}, {"$set": {"enabled": False}})
        return True

    @staticmethod
    async def save(rotation):
        await COL.update_one({"id": rotation.id}, {"$set": {
            "account_id": rotation.account_id, "enabled": rotation.enabled,
            "interval": rotation.interval, "current_index": rotation.current_index,
            "last_changed": rotation.last_changed or datetime.utcnow()
        }})
