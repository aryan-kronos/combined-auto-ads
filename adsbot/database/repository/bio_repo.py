# [Engineered & Developed by Aryan | https://t.me/thatonearyan]
from datetime import datetime
from database.session import db, get_next_id
from database.models.bio import Bio

COL = db.bios

def _obj(d): return Bio(**{k: d.get(k) for k in ("id","user_id","text","created_at")})

class BioRepository:
    @staticmethod
    async def add(user_id: int, text: str):
        d = {"id": await get_next_id("bios"), "user_id": user_id, "text": text, "created_at": datetime.utcnow()}
        await COL.insert_one(d)
        return _obj(d)

    @staticmethod
    async def get_bios(user_id: int):
        return [_obj(d) async for d in COL.find({"user_id": user_id})]

    @staticmethod
    async def count(user_id: int):
        return await COL.count_documents({"user_id": user_id})

    @staticmethod
    async def delete(bio_id: int):
        await COL.delete_one({"id": bio_id})
        await db.bio_rotation_items.delete_many({"bio_id": bio_id})

    @staticmethod
    async def get_by_id(bio_id: int):
        d = await COL.find_one({"id": bio_id})
        return _obj(d) if d else None
