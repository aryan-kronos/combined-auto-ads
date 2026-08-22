# [Engineered & Developed by Aryan | https://t.me/thatonearyan]
from datetime import datetime
from database.session import db, get_next_id
from database.models.account import Account
from database.models.user import User

ACCOUNTS = db.accounts
USERS = db.users

def _acc(d):
    return Account(**{k: d.get(k) for k in (
        "id","user_id","account_name","phone","session_string",
        "active_campaign","active","created_at"
    )})

def _user(d):
    return User(**{k: d.get(k) for k in (
        "id","telegram_id","username","first_name","account_slots","wallet",
        "is_premium","custom_bio","is_banned","created_at"
    )})

class AccountRepository:
    @staticmethod
    async def get_user(telegram_id: int):
        d = await USERS.find_one({"telegram_id": telegram_id})
        return _user(d) if d else None

    @staticmethod
    async def get_account(account_id: int):
        d = await ACCOUNTS.find_one({"id": account_id})
        return _acc(d) if d else None

    @staticmethod
    async def get_user_by_id(user_id: int):
        d = await USERS.find_one({"id": user_id})
        return _user(d) if d else None

    @staticmethod
    async def count_accounts(user_id: int):
        return await ACCOUNTS.count_documents({"user_id": user_id})

    @staticmethod
    async def get_accounts(user_id: int):
        docs = [d async for d in ACCOUNTS.find({"user_id": user_id})]
        seen, out = set(), []
        for d in docs:
            s = d.get("session_string")
            if s in seen:
                continue
            seen.add(s)
            out.append(_acc(d))
        return out

    get_user_accounts = get_accounts

    @staticmethod
    async def add_account(user_id: int, account_name: str, phone: str, session_string: str):
        doc = {
            "id": await get_next_id("accounts"),
            "user_id": user_id,
            "account_name": account_name,
            "phone": phone,
            "session_string": session_string,
            "active_campaign": False,
            "active": True,
            "created_at": datetime.utcnow(),
        }
        await ACCOUNTS.insert_one(doc)
        print("ACCOUNT SAVED FOR USER:", user_id)
        return _acc(doc)

    @staticmethod
    async def delete_account(account_id: int):
        await ACCOUNTS.delete_one({"id": account_id})
        # Preserve SQL CASCADE behavior.
        await db.campaigns.delete_many({"account_id": account_id})
        await db.bio_rotations.delete_many({"account_id": account_id})

    @staticmethod
    async def update_status(account_id: int, status: bool):
        r = await ACCOUNTS.update_one({"id": account_id}, {"$set": {"active": status}})
        return r.matched_count > 0

    @staticmethod
    async def get_active_accounts():
        return [_acc(d) async for d in ACCOUNTS.find({"active": True})]
