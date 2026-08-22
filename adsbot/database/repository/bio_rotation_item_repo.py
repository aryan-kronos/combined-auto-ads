# [Engineered & Developed by Aryan | https://t.me/thatonearyan]
from database.session import db, get_next_id
from database.models.bio_rotation_item import BioRotationItem

COL = db.bio_rotation_items

def _obj(d): return BioRotationItem(**{k: d.get(k) for k in ("id","rotation_id","bio_id")})

class BioRotationItemRepository:
    @staticmethod
    async def add(rotation_id: int, bio_id: int):
        d = {"id": await get_next_id("bio_rotation_items"), "rotation_id": rotation_id, "bio_id": bio_id}
        await COL.insert_one(d)
        return _obj(d)

    @staticmethod
    async def get_bios(rotation_id: int):
        return [_obj(d) async for d in COL.find({"rotation_id": rotation_id})]

    @staticmethod
    async def clear(rotation_id: int):
        await COL.delete_many({"rotation_id": rotation_id})

    @staticmethod
    async def delete_bio(bio_id: int):
        await COL.delete_many({"bio_id": bio_id})
