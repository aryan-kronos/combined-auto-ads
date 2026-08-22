from __future__ import annotations
import certifi
# [Engineered & Developed by Aryan | https://t.me/thatonearyan]

import os
from typing import Any

from dotenv import load_dotenv
from pymongo import AsyncMongoClient, ASCENDING, ReturnDocument
from pymongo.errors import PyMongoError

load_dotenv()

def _clean_uri(raw: str) -> str:
    if not raw:
        return "mongodb+srv://pfparyan_db_user:9EoNNlZ4aCEaD0Nh@cluster0.czoripk.mongodb.net/?retryWrites=true&w=majority"
    u = raw.strip().strip('"').strip("'").strip()
    if not (u.startswith("mongodb://") or u.startswith("mongodb+srv://")):
        return "mongodb+srv://pfparyan_db_user:9EoNNlZ4aCEaD0Nh@cluster0.czoripk.mongodb.net/?retryWrites=true&w=majority"
    if ".mongodb/" in u:
        u = u.replace(".mongodb/", ".mongodb.net/")
    elif u.endswith(".mongodb"):
        u = u + ".net"
    return u

MONGO_URI = _clean_uri(os.getenv("MONGO_URI", ""))
DB_NAME = os.getenv("ADS_DB_NAME") or os.getenv("DB_NAME", "tgbitz_ads_bot").strip()

client = AsyncMongoClient(
    MONGO_URI,
    tlsCAFile=certifi.where(),
    serverSelectionTimeoutMS=10000,
    connectTimeoutMS=10000,
    socketTimeoutMS=20000,
    maxPoolSize=20,
    minPoolSize=1,
)

db = client[DB_NAME]


async def get_next_id(sequence_name: str) -> int:
    doc = await db.counters.find_one_and_update(
        {"_id": sequence_name},
        {"$inc": {"value": 1}},
        upsert=True,
        return_document=ReturnDocument.AFTER,
    )
    return int(doc["value"])


async def init_db() -> None:
    await client.admin.command("ping")

    # Important lookup indexes.
    await db.users.create_index([("telegram_id", ASCENDING)], unique=True)
    await db.accounts.create_index([("user_id", ASCENDING)])
    await db.accounts.create_index([("active", ASCENDING)])
    await db.campaigns.create_index([("account_id", ASCENDING)])
    await db.campaigns.create_index([("running", ASCENDING)])
    await db.campaign_targets.create_index([("campaign_id", ASCENDING)])
    await db.bios.create_index([("user_id", ASCENDING)])
    await db.bio_rotations.create_index([("account_id", ASCENDING)])
    await db.bio_rotations.create_index([("enabled", ASCENDING)])
    await db.bio_rotation_items.create_index([("rotation_id", ASCENDING)])
    await db.bio_rotation_items.create_index([("bio_id", ASCENDING)])
    await db.bot_settings.create_index([("page", ASCENDING)], unique=True)

    print(f"✅ MongoDB connected: {DB_NAME}")


async def close_db() -> None:
    client.close()
