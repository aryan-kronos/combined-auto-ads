# [Engineered & Developed by Aryan | https://t.me/thatonearyan]
from dataclasses import dataclass
from datetime import datetime

@dataclass
class User:
    id: int
    telegram_id: int
    username: str | None = None
    first_name: str = ""
    account_slots: int = 1
    wallet: int = 0
    is_premium: bool = False
    custom_bio: str | None = None
    is_banned: bool = False
    created_at: datetime | None = None
